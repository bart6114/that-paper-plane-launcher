from geometry import *
import uuid

def project(groups,path,settings):
 ET.register_namespace('',NS['m']);N='{'+NS['m']+'}'
 r=ET.Element(N+'model',{'unit':'millimeter','xmlns:BambuStudio':'http://schemas.bambulab.com/package/2021'})
 ET.SubElement(r,N+'metadata',{'name':'Application'}).text='BambuStudio-02.08.02.61'
 ET.SubElement(r,N+'metadata',{'name':'BambuStudio:3mfVersion'}).text='1'
 ET.SubElement(r,N+'metadata',{'name':'Title'}).text='That Paper Plane Launcher — prototype'
 res=ET.SubElement(r,N+'resources');buildel=ET.SubElement(r,N+'build');cfg=ET.Element('config');oid=1
 for plate_i,(label,items) in enumerate(groups,1):
  plate=ET.SubElement(cfg,'plate')
  for k,v in [('plater_id',str(plate_i)),('plater_name',label),('locked','false')]:ET.SubElement(plate,'metadata',{'key':k,'value':v})
  px=(plate_i-1)*307.2
  for name,mm,x,y in items:
   m=mm.copy();m.apply_translation((x,y,0))
   ob=ET.SubElement(res,N+'object',{'id':str(oid),'type':'model'});me=ET.SubElement(ob,N+'mesh');ve=ET.SubElement(me,N+'vertices');fa=ET.SubElement(me,N+'triangles')
   for vx,vy,vz in m.vertices:ET.SubElement(ve,N+'vertex',{'x':f'{vx:.7f}','y':f'{vy:.7f}','z':f'{vz:.7f}'})
   for a,b,c in m.faces:ET.SubElement(fa,N+'triangle',{'v1':str(a),'v2':str(b),'v3':str(c)})
   comp=ET.SubElement(res,N+'object',{'id':str(oid+1),'type':'model'});cs=ET.SubElement(comp,N+'components');ET.SubElement(cs,N+'component',{'objectid':str(oid)})
   ET.SubElement(buildel,N+'item',{'objectid':str(oid+1),'transform':f'1 0 0 0 1 0 0 0 1 {px} 0 0','printable':'1'})
   o=ET.SubElement(cfg,'object',{'id':str(oid+1)});ET.SubElement(o,'metadata',{'key':'name','value':name});ET.SubElement(o,'metadata',{'key':'extruder','value':'1'})
   if name=='Retrofit_Slider':
    for k,v in [('wall_loops','10'),('brim_type','outer_only'),('brim_width','5'),('brim_object_gap','0.1')]:ET.SubElement(o,'metadata',{'key':k,'value':v})
   pp=ET.SubElement(o,'part',{'id':str(oid),'subtype':'normal_part'});ET.SubElement(pp,'metadata',{'key':'name','value':name});ET.SubElement(pp,'metadata',{'key':'matrix','value':'1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1'});ET.SubElement(pp,'mesh_stat',{'face_count':str(len(m.faces)),'edges_fixed':'0','degenerate_facets':'0','facets_removed':'0','facets_reversed':'0','backwards_edges':'0'})
   inst=ET.SubElement(plate,'model_instance')
   for k,v in [('object_id',str(oid+1)),('instance_id','0'),('identify_id',str(oid+100))]:ET.SubElement(inst,'metadata',{'key':k,'value':v})
   oid+=2
 proj=json.loads((Path(__file__).parent/'data/printer_defaults.json').read_text())
 proj.update(settings)
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
  for n,d in [('[Content_Types].xml','content_types.xml'),('_rels/.rels','relationships.xml')]:
   z.writestr(n,(Path(__file__).parent/'data'/d).read_bytes())
  z.writestr('3D/3dmodel.model',ET.tostring(r,encoding='utf-8',xml_declaration=True));z.writestr('Metadata/model_settings.config',ET.tostring(cfg,encoding='utf-8',xml_declaration=True));z.writestr('Metadata/project_settings.config',json.dumps(proj,indent=2))
