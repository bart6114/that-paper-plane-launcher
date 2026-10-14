from geometry import *
import hashlib
out=Path(__file__).resolve().parent.parent/'build'
old=dict(trimesh.load(Path(__file__).parent/'data/accepted_assembly.3mf',force='scene').geometry)
new=dict(trimesh.load(out/'checks/assembly_geometry.3mf',force='scene').geometry)
assert set(old)==set(new) and len(new)==11
for n,m in new.items():
 assert np.array_equal(m.vertices,old[n].vertices) and np.array_equal(m.faces,old[n].faces)
 assert m.is_volume and len(m.split())==1 and m.nondegenerate_faces().all() and m.unique_faces().all()
 for extn in ['3mf','stl']:
  re=trimesh.load(out/'parts'/f'{n}.{extn}',force='mesh');assert re.is_volume and len(re.split())==1 and abs(re.volume-m.volume)<.03
m=trimesh.load(out/'parts/Retrofit_Slider.3mf',force='mesh')
assert np.allclose(m.extents,[37.6,24.20927,34.4],atol=.001),m.extents
assert abs(m.bounds[0,2])<1e-6
for file,count in [('Launcher_P1S.3mf',11),('Base_Only_P1S.3mf',1),('Slider_Only_P1S.3mf',1)]:
 with zipfile.ZipFile(out/file) as z:
  assert z.testzip() is None
  for n in z.namelist():
   if n.endswith(('.xml','.model','.rels')):ET.fromstring(z.read(n))
 sc=trimesh.load(out/file,force='scene');assert len(sc.geometry)==count
r={'assembly_geometry_exactly_unchanged_from_flush_body':True,'upright_slider_dimensions_mm':m.extents.tolist(),'orientation':'front end on bed; axis X vertical; no 45 degree tilt','geometry':'pass','export_roundtrip':'pass','project_counts':[11,1,1],'motion_checks':'Run verify_motion.py for scoped FCL motion checks.','physical_strength_and_surface_friction':'unchecked'}
(out/'checks/layout_verification.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
