from print_package import *
import hashlib
from shapely.geometry import LineString,Point
from model import build_parts
OUT=Path(__file__).resolve().parent.parent/'build'
for directory in ['parts','checks','individual']:(OUT/directory).mkdir(parents=True,exist_ok=True)
p=build_parts()
for n in ['Retrofit_Slider','Retrofit_Sear']:p[n].export(OUT/'checks'/(n+'.stl'))
export_3mf(p,OUT/'checks/assembly_geometry.3mf')

settings=json.loads((Path(__file__).parent/'data/print_settings.json').read_text());settings['print_settings_id']='Reviewed layout — P1S 0.4, PLA, 0.20 mm'
positions={'Finger_Trigger':(50,88),'Retrofit_Sear':(82,88),'Retrofit_Slider':(50,132),'Front_Anchor':(101,132),'Rear_Key':(177,88),'Grip_Key':(201,88),'Front_Lock_Pin_Lower':(153,128),'Rear_Keeper_Pin':(178,127),'Grip_Keeper_Pin':(202,127)}
printed={};checks={}
for name,m in p.items():
 pm=print_mesh('Slider' if name=='Retrofit_Slider' else name,m)
 if name=='Retrofit_Slider':
  pm=m.copy();pm.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2,[0,1,0]));pm.apply_translation(-pm.bounds[0])
 assert np.isclose(m.volume,pm.volume,atol=1e-4)
 assert np.array_equal(m.faces,pm.faces)
 assert np.allclose(m.edges_unique_length,pm.edges_unique_length,atol=1e-6)
 printed[name]=pm
 pm.export(OUT/'parts'/f'{name}.stl');export_3mf({name:pm},OUT/'parts'/f'{name}.3mf')
 checks[name]={'rigid_transform_only':True,'watertight':bool(pm.is_watertight),'positive_volume_mm3':float(pm.volume),'connected_bodies':len(pm.split()),'orientation':'Upright, flat front end down; print layer normal is assembly X' if name=='Retrofit_Slider' else 'previous orientation'}
 for ext in ['stl','3mf']:
  re=trimesh.load(OUT/'parts'/f'{name}.{ext}',force='mesh');assert re.is_volume and len(re.split())==1
halves=[(n,printed[n],6,y) for n,y in [('Base',17),('Cover',137)]]
small=[(n,printed[n],x,y) for n,(x,y) in positions.items()]
for group in [halves,small]:
 boxes=[]
 for n,m,x,y in group:
  b=m.bounds+np.array([x,y,0]);assert np.all(b[0]>=-1e-6) and np.all(b[1]<=256)
  boxes.append((n,b))
 for i,(n,a) in enumerate(boxes):
  for k,b in boxes[i+1:]:
   gap=np.maximum(np.maximum(a[0,:2]-b[1,:2],b[0,:2]-a[1,:2]),0)
   assert np.linalg.norm(gap)>=8,(n,k,gap)
project([('Shells exterior face down',halves),('Reviewed small parts',small)],OUT/'Launcher_P1S.3mf',settings)
individual_projects=[]
for name,pm in printed.items():
 # Center each individual part on its own plate, retaining its full-project orientation.
 x,y=(256-pm.extents[:2])/2
 assert x>=0 and y>=0
 file=f'individual/{name}_P1S.3mf'
 project([(name.replace('_',' '),[(name,pm,float(x),float(y))])],OUT/file,settings)
 individual_projects.append((file,1))
for file,expected in [('Launcher_P1S.3mf',len(p))]+individual_projects:
 scene=trimesh.load(OUT/file,force='scene');assert len(scene.geometry)==expected
 for mesh in scene.geometry.values():assert mesh.is_volume and len(mesh.split())==1
(OUT/'checks/layout_validation.json').write_text(json.dumps({'parts':checks,'project_object_counts':[len(p)]+[1]*len(p),'minimum_xy_bounding_box_gap_mm':8,'bed_bounds_mm':[0,256],'geometry_changed':'No assembly shape changes; complete individual-part print set'},indent=2))
print('Built full project and all 11 individual-part projects; geometry, reopen and placement checks pass.')

scene=trimesh.Scene()
for n,m in p.items():
 mm=m.copy()
 if n=='Retrofit_Slider':mm.apply_translation((99.536,0,0))
 mm.visual.face_colors=trimesh.visual.color.hex_to_rgba('#85aeb7' if n in ['Base','Cover'] else '#d9ad66')
 scene.add_geometry(mm,node_name=n,geom_name=n)
scene.export(OUT/'Assembly_Inspection.glb')
