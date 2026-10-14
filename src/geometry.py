"""Millimetres. Source-derived parametric mesh CSG; no B-rep master exists."""
from pathlib import Path
import sys, json, zipfile, xml.etree.ElementTree as ET
import numpy as np, trimesh, manifold3d as mf
NS={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
ROOT=Path(__file__).resolve().parent.parent

PINS=[(38.6,20.0582256),(71.,25.8297558),(104.005704,34.7815628)]
D={11:(42.1435146,10.2082253,0),5:(77.,24.8296413,0),13:(110.8551292,35.6366453,0)}
PARAM={'transverse_scale':1.5,'outer_skin_mm':3.8,'pivot_diameters_mm':[3.4,4.4,4.4],'pivot_bores_mm':[3.9,4.9,4.9],'key_clearance_mm':.30,'slider_rail_offset_mm':.30,'eye_outer_radius_mm':4.8,'eye_hole_radius_mm':1.8,'front_pin_slot_width_mm':1.4,'front_pin_slot_root_z_mm':0.0,'keeper_slot_width_mm':1.2,'keeper_slot_root_z_mm':-4.5}
def man(m):
 a=mf.Manifold(mf.Mesh64(np.array(m.vertices,dtype=np.float64),np.array(m.faces,dtype=np.uint64)));assert a.status()==mf.Error.NoError;return a

def mesh(a):
 assert a.status()==mf.Error.NoError
 r=a.set_tolerance(.001).simplify(.001).to_mesh64();m=trimesh.Trimesh(np.array(r.vert_properties)[:,:3],r.tri_verts,process=False)
 assert m.is_volume,(m.is_watertight,m.volume);return m

def box(x0,x1,y0,y1,z0,z1):return mf.Manifold.cube((x1-x0,y1-y0,z1-z0)).translate((x0,y0,z0))
def cyl(x,y,z0,z1,r,r2=None,n=64):return mf.Manifold.cylinder(z1-z0,r,r if r2 is None else r2,n).translate((x,y,z0))
def ext(sec,z0,z1):return sec.extrude(z1-z0).translate((0,0,z0))
def rr(x,y,w,h,r):
 s=mf.CrossSection.square((w-2*r,h),True)+mf.CrossSection.square((w,h-2*r),True)
 for dx in [-w/2+r,w/2-r]:
  for dy in [-h/2+r,h/2-r]:s+=mf.CrossSection.circle(r,32).translate((dx,dy))
 return s.translate((x,y))
def placed_slider(m,x=0):
 v=m.vertices;return trimesh.Trimesh(np.c_[-v[:,2]+x,v[:,1]+47.84046,v[:,0]*1.5],m.faces,process=True)
def cover_assembled(m):
 m=m.copy();m.vertices=m.vertices*[-1,1,-1]+[0,0,1.1];return m

def dovetail(y,clear=0):
 # Profile in YZ; broad wings trapped inside each shell, continuous 4 mm web.
 poly=np.array([[-4,-5.8],[4,-5.8],[4,-3.8],[2,-1.5],[2,1.5],[4,3.8],[4,5.8],[-4,5.8],[-4,3.8],[-2,1.5],[-2,-1.5],[-4,-3.8]])
 s=mf.CrossSection([poly]).offset(clear)
 # local x=Y, y=Z, extrude z=X
 return s.extrude(9.5+clear).rotate((90,0,90)).translate((114-clear,y,0))

def export_3mf(parts,path):
 scene=trimesh.Scene()
 for name,m in parts.items():scene.add_geometry(m,node_name=name,geom_name=name)
 import io
 raw=trimesh.exchange.threemf.export_3MF(scene)
 with zipfile.ZipFile(io.BytesIO(raw)) as src,zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as dst:
  for n in src.namelist():
   data=src.read(n)
   if n.endswith('.model'):
    root=ET.fromstring(data)
    for e in root.iter():
     for k in list(e.attrib):
      if k.endswith('UUID'):del e.attrib[k]
    data=ET.tostring(root,encoding='utf-8',xml_declaration=True)
   dst.writestr(n,data)

def print_mesh(name,m):
 m=m.copy()
 if name=='Cover':m.apply_transform(trimesh.transformations.rotation_matrix(np.pi,[1,0,0]))
 elif name=='Slider':m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
 elif name=='Front_Anchor':m.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2,[0,1,0]))
 elif 'Key' in name:m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
 elif 'Keeper' in name or 'Lock_Pin' in name:m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
 m.apply_translation([-m.bounds[0,0],-m.bounds[0,1],-m.bounds[0,2]])
 return m
