from geometry import *
import fcl,hashlib,importlib.metadata
OUT=Path(__file__).resolve().parent.parent/'build'
p=dict(trimesh.load(OUT/'checks/assembly_geometry.3mf',force='scene').geometry);old=dict(trimesh.load(Path(__file__).parent/'data/assembly_seed.3mf',force='scene').geometry)
r={'evidence_level':'E1 CAD verified with scoped FCL motion evidence; physical performance unverified','geometry':{},'unchanged_parts':{},'tool_versions':{n:importlib.metadata.version(n) for n in ['trimesh','manifold3d','python-fcl']}}
for n,m in p.items():
 info={'watertight':bool(m.is_watertight),'single_connected_body':len(m.split())==1,'positive_volume_mm3':float(m.volume),'duplicate_faces':int(len(m.faces)-sum(m.unique_faces())),'degenerate_faces':int(sum(~m.nondegenerate_faces(height=1e-7)))}
 assert m.is_volume and info['single_connected_body'] and not info['duplicate_faces'] and not info['degenerate_faces'] and man(m).status()==mf.Error.NoError
 r['geometry'][n]=info
 if n!='Base':
  same=np.array_equal(old[n].vertices,m.vertices) and np.array_equal(old[n].faces,m.faces);assert same;r['unchanged_parts'][n]=True
for n,m in p.items():
 for extension in ['stl','3mf']:
  re=trimesh.load(OUT/'parts'/f'{n}.{extension}',force='mesh');assert re.is_volume and len(re.split())==1
# Additive-only edit, constrained to the four ends and the underside wall.
base=man(p['Base']);prior=man(old['Base']);added=base-prior
assert abs((prior-base).volume())<.001
mask=box(1.099,16.131,16.5581,18.5583,-4.511,4.501)
posts=[]
for x,y,top in [(*xy,7.6) for xy in PINS]+[(105.6822,-42.31353,6.3)]:
 mask+=box(x-4.001,x+4.001,y-4.001,y+4.001,top-.021,8.301)
 bounds=(base^box(x-.5,x+.5,y-.5,y+.5,0,10)).bounding_box()
 assert abs(bounds[5]-8.3)<1e-5
 posts.append({'xy_mm':[x,y],'old_end_z_mm':top,'new_end_z_mm':bounds[5],'extension_mm':8.3-top})
assert abs((added-mask).volume())<.002 # mesh round-trip tolerance, mm3
wall=box(1.112801,16.1128,16.558201,18.558201,-4.5,4.49)
assert abs((wall-base).volume())<.001
r['edits']={'posts':posts,'underside_wall_thickness_mm':2,'added_volume_mm3':added.volume(),'only_base_changed':True}
# New material has no interference with any other assembled part.
r['added_material_intersections_mm3']={n:float((added^man(m)).volume()) for n,m in p.items() if n!='Base'}
assert max(abs(v) for v in r['added_material_intersections_mm3'].values())<.001
def obj(m):
 mo=fcl.BVHModel();mo.beginModel(len(m.vertices),len(m.faces));mo.addSubModel(m.vertices,m.faces);mo.endModel();return fcl.CollisionObject(mo)
def dist(a,b):return float(fcl.distance(a,b,fcl.DistanceRequest(),fcl.DistanceResult()))
fixed={n:obj(p[n]) for n in ['Base','Cover','Front_Anchor','Front_Lock_Pin_Lower','Rear_Key','Grip_Key','Rear_Keeper_Pin','Grip_Keeper_Pin']};slider=obj(p['Retrofit_Slider']);worst=(1e9,None,None)
for x in np.linspace(-101,105,2061):
 slider.setTranslation(np.array([x,0.,0.]))
 for n,ob in fixed.items():
  d=dist(slider,ob)
  if d<worst[0]:worst=(d,n,float(x))
assert worst[0]>.15,worst
r['slider_full_travel_fixed_parts']={'x_range_mm':[-101,105],'sample_step_max_mm':.1,'worst_gap_mm_pair_x':worst,'between_sample_bound_mm':.05,'assumed_surface_error_mm':.1,'remaining_margin_mm':worst[0]-.15}
P=np.array([*PINS[2],0]);fm=man(p['Base'])+man(p['Cover']);frame=obj(mesh(fm));rows=[]
for dz in [0,-.25,.25]:
 m=p['Retrofit_Sear'].copy();m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(-5.8),[0,0,1],P));m.apply_translation([0,0,dz]);ob=obj(m);worst=(1e9,None)
 for x in np.linspace(-101,99.534,2007):
  slider.setTranslation(np.array([x,0.,-.3 if dz>0 else .3 if dz<0 else 0]));d=dist(slider,ob)
  if d<worst[0]:worst=(d,float(x))
 overlap=float((man(m)^fm).volume());assert abs(overlap)<.001;assert worst[0]>.15
 rows.append({'angle_deg':-5.8,'catch_z_offset_mm':dz,'slider_z_offset_mm':-.3 if dz>0 else .3 if dz<0 else 0,'slider_x_range_mm':[-101,99.534],'max_sample_step_mm':.1,'minimum_slider_catch_gap_mm_x':worst,'between_sample_bound_mm':.05,'assumed_total_clearance_loss_mm':.1,'remaining_slider_margin_mm':worst[0]-.15,'housing_intersection_mm3':overlap,'note':'Catch collar contact at axial endplay is intended.'})
r['release_checks']=rows
r['packages']={}
for path in list(OUT.glob('*.3mf'))+list((OUT/'parts').glob('*.3mf')):
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None
  for nn in z.namelist():
   if nn.endswith(('.xml','.model','.rels')):ET.fromstring(z.read(nn))
 scene=trimesh.load(path,force='scene')
 for m in scene.geometry.values():assert m.is_volume and len(m.split())==1
 r['packages'][str(path.relative_to(OUT))]={'mesh_count':len(scene.geometry),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
# Sweep actual moving meshes against just the newly added material.
# Existing pivot contacts are intentionally unchanged.
# Restrict Boolean differences to the designed features, excluding sub-micron
# numerical slivers from the source mesh round-trip elsewhere on the shell.
feature_mask=box(1.10,16.13,16.558201,18.558201,-4.51,4.5)
for x,y,top in [(*xy,7.6) for xy in PINS]+[(105.6822,-42.31353,6.3)]:
 feature_mask+=box(x-4,x+4,y-4,y+4,top+.00001,8.30001)
r['excluded_roundtrip_sliver_volume_mm3']=float((added-feature_mask).volume())
assert abs(r['excluded_roundtrip_sliver_volume_mm3'])<.003
new_ob=obj(mesh(added^feature_mask));sweeps=[]
for name,pivot,lo,hi in [('Finger_Trigger',PINS[0],-20,60),('Retrofit_Sear',PINS[2],-15,10)]:
 worst=(1e9,None)
 for angle in np.linspace(lo,hi,int((hi-lo)/.1)+1):
  m=p[name].copy();m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(angle),[0,0,1],[*pivot,0]))
  d=dist(obj(m),new_ob)
  if d<worst[0]:worst=(d,float(angle))
 radius=np.linalg.norm(p[name].vertices-np.array([*pivot,0]),axis=1).max()
 bound=float(radius*np.radians(.05))
 print(name,worst,bound,flush=True)
 assert worst[0]-bound-.1>0
 sweeps.append({'part':name,'angle_range_deg':[lo,hi],'sample_step_deg':.1,'worst_gap_mm_angle':worst,'between_sample_bound_mm':bound,'assumed_clearance_loss_mm':.1,'remaining_margin_mm':worst[0]-bound-.1})
r['moving_parts_vs_added_material']=sweeps
r['gates']={'geometry':'pass','fixed_part_travel':'pass','release_clearance':'pass','printed_strength_and_fatigue':'unchecked','physical_function':'unchecked','full_grip_envelope':'unchecked'}
(OUT/'checks/validation.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if k not in ['geometry','packages']},indent=2))
