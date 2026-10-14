"""Millimetre mesh-CSG model; base changes applied to the frozen accepted seed."""
from geometry import *

def build_parts():
 params=json.loads((Path(__file__).parent/'data/model_parameters.json').read_text())
 p=dict(trimesh.load(Path(__file__).parent/'data/assembly_seed.3mf',force='scene').geometry)
 # Four integral posts extended to the cover exterior, without changing their fit.
 base=man(p['Base'])
 POSTS=[(*xy,7.6) for xy in PINS]+[(105.6822,-42.31353,6.3)]
 for x,y,old_top in POSTS:
  local=base ^ box(x-4,x+4,y-4,y+4,old_top-.03,old_top+.01)
  sec=local.slice(old_top-.01)
  base += ext(sec,old_top-.02,params["post_end_z_mm"])
 # Restore the interrupted 2 mm bottom wall; same transverse span as adjacent wall.
 base += box(*params["underside_wall_box_mm"])
 raw=base.set_tolerance(.00001).simplify(.00001).to_mesh64()
 m=trimesh.Trimesh(np.array(raw.vert_properties)[:,:3],raw.tri_verts,process=False)
 m.vertices=np.round(m.vertices,6);m.merge_vertices();m.update_faces(m.nondegenerate_faces(height=1e-7));m.update_faces(m.unique_faces());m.remove_unreferenced_vertices()
 assert m.is_volume and len(m.split())==1
 p['Base']=m
 return p
