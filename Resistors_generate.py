#!/usr/bin/env python

import sys
import os
import math

# ensure that the kicad-footprint-generator directory is available
sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory

from KicadModTree import *  # NOQA

def roundG(x, g):
    if (x>0):
        return math.ceil(x/g)*g
    else:
        return math.floor(x/g)*g


def roundCrt(x):
    return roundG(x, 0.05)

def makeRES_SIMPLE(rm, rmdisp, rl, rw, rh, ddrill, footprint_namepart, description, tags, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname=""):
        padx=2*ddrill
        pady=padx
        crt_offset=0.25
        slk_offset=0.15
        lw_fab=0.1
        lw_crt=0.05
        lw_slk=0.15
        txt_offset=1

        w=rl
        h=max(rw,rh)
        left=(rm-rl)/2
        top=-h/2
        h_slk=h+2*slk_offset
        w_slk=rl+2*slk_offset
        l_slk=left-slk_offset
        r_slk=l_slk+w_slk
        t_slk=-h_slk/2
        w_crt=rm+padx+2*crt_offset
        h_crt=max(h_slk, pady)+2*crt_offset
        l_crt=min(l_slk, -padx/2)-crt_offset
        t_crt=min(t_slk, -pady/2)-crt_offset
        
        
        lib_name = "Resistors_ThroughHole"
        footprint_name="Resistor{0}_RM{1}mm".format(footprint_namepart,rmdisp)
        if (specialfpname!=""):
            footprint_name=specialfpname;
        print(footprint_name)

        # init kicad footprint
        kicad_mod = Footprint(footprint_name)
        kicad_mod.setDescription(description)
        kicad_mod.setTags(tags)

        # set general values
        kicad_mod.append(Text(type='reference', text='REF**', at=[rm/2, t_slk-txt_offset], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text=footprint_name, at=[rm/2, h_slk/2+txt_offset], layer='F.Fab'))

        # create FAB-layer
        kicad_mod.append(RectLine(start=[left, top], end=[left+w, top+h], layer='F.Fab', width=lw_fab))
        kicad_mod.append(Line(start=[0, 0], end=[left, 0], layer='F.Fab', width=lw_fab))
        kicad_mod.append(Line(start=[rm, 0], end=[left+w, 0], layer='F.Fab', width=lw_fab))

        # create SILKSCREEN-layer
        kicad_mod.append(RectLine(start=[l_slk, t_slk], end=[l_slk+w_slk, t_slk+h_slk], layer='F.SilkS'))
        kicad_mod.append(Line(start=[padx/2+0.3, 0], end=[l_slk, 0], layer='F.SilkS'))
        kicad_mod.append(Line(start=[rm-padx/2-0.3, 0], end=[l_slk+w_slk, 0], layer='F.SilkS'))

        # create courtyard
        kicad_mod.append(RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt+w_crt), roundCrt(t_crt+h_crt)], layer='F.CrtYd', width=lw_crt))

        # create pads 
        kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[0, 0], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))
        kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[rm, 0], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))

        # add model
        if (has3d!=0):
            kicad_mod.append(Model(filename=lib_name + ".3dshapes/"+footprint_name+".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))

        # print render tree
        # print(kicad_mod.getRenderTree())
        # print(kicad_mod.getCompleteRenderTree())

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile(footprint_name+'.kicad_mod')


def makeRES(rm, rmdisp, rl, rw, rh, ddrill, footprint_namepart, description, tags, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname=""):
        padx=2*ddrill
        pady=padx
        crt_offset=0.25
        slk_offset=0.15
        lw_fab=0.1
        lw_crt=0.05
        lw_slk=0.15
        txt_offset=1

        w=rl
        h=max(rw,rh)
        left=(rm-rl)/2
        top=-h/2
        h_slk=h+2*slk_offset
        w_slk=rl+2*slk_offset
        l_slk=left-slk_offset
        r_slk=l_slk+w_slk
        t_slk=-h_slk/2
        w_crt=rm+padx+2*crt_offset
        h_crt=max(h_slk, pady)+2*crt_offset
        l_crt=min(l_slk, -padx/2)-crt_offset
        t_crt=min(t_slk, -pady/2)-crt_offset
        
        
        lib_name = "Resistors_ThroughHole"
        if (specialfpname!=""):
            footprint_name=specialfpname;
        else:
            footprint_name="Resistor{0}_L{2}mm-W{3}mm-H{4}mm-p{1}mm".format(footprint_namepart,rmdisp,rl,rw,rh)
        print(footprint_name)

        # init kicad footprint
        kicad_mod = Footprint(footprint_name)
        kicad_mod.setDescription(description)
        kicad_mod.setTags(tags)

        # set general values
        kicad_mod.append(Text(type='reference', text='REF**', at=[rm/2, t_slk-txt_offset], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text=footprint_name, at=[rm/2, h_slk/2+txt_offset], layer='F.Fab'))

        # create FAB-layer
        kicad_mod.append(RectLine(start=[left, top], end=[left+w, top+h], layer='F.Fab', width=lw_fab))
        kicad_mod.append(Line(start=[0, 0], end=[left, 0], layer='F.Fab', width=lw_fab))
        kicad_mod.append(Line(start=[rm, 0], end=[left+w, 0], layer='F.Fab', width=lw_fab))

        # create SILKSCREEN-layer
        kicad_mod.append(RectLine(start=[l_slk, t_slk], end=[l_slk+w_slk, t_slk+h_slk], layer='F.SilkS'))
        kicad_mod.append(Line(start=[padx, 0], end=[l_slk, 0], layer='F.SilkS'))
        kicad_mod.append(Line(start=[rm-padx, 0], end=[l_slk+w_slk, 0], layer='F.SilkS'))

        # create courtyard
        kicad_mod.append(RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt+w_crt), roundCrt(t_crt+h_crt)], layer='F.CrtYd', width=lw_crt))

        # create pads 
        kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[0, 0], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))
        kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[rm, 0], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))

        # add model
        if (has3d!=0):
            kicad_mod.append(Model(filename=lib_name + ".3dshapes/"+footprint_name+".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))

        # print render tree
        # print(kicad_mod.getRenderTree())
        # print(kicad_mod.getCompleteRenderTree())

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile(footprint_name+'.kicad_mod')


def makeRES_VERT(rm, rmdisp, rl, rw, rh, ddrill, footprint_namepart, description, tags, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0):
        padx=2*ddrill
        pady=padx
        if (largepadsx):
            padx=max(padx, largepadsx)
        if (largepadsy):
            pady=max(pady, largepadsy)
        crt_offset=0.25
        slk_offset=0.15
        lw_fab=0.1
        lw_crt=0.05
        lw_slk=0.15
        txt_offset=1

        w=rw
        h=rh
        left=-(rw-rm)/2
        top=-h/2
        h_slk=h+2*slk_offset
        w_slk=w+2*slk_offset
        l_slk=left-slk_offset
        r_slk=l_slk+w_slk
        t_slk=-h_slk/2
        xl1_slk=left+(rw-rh)/2
        xl2_slk=xl1_slk+rh
        w_crt=w_slk+2*crt_offset
        h_crt=h_slk+2*crt_offset
        l_crt=l_slk-crt_offset
        t_crt=t_slk-crt_offset
        
        
        lib_name = "Resistors_ThroughHole"
        if (specialfpname=="SIMPLE"):
            footprint_name="Resistor{0}_RM{1}mm".format(footprint_namepart,rmdisp)
        else:
            if (specialfpname!=""):
                footprint_name=specialfpname;
            else:
                footprint_name="Resistor{0}_W{2}mm-H{3}mm-L{4}mm-p{1}mm".format(footprint_namepart,rmdisp,rw,rh, rl)
        print(footprint_name)

        # init kicad footprint
        kicad_mod = Footprint(footprint_name)
        kicad_mod.setDescription(description)
        kicad_mod.setTags(tags)

        # set general values
        kicad_mod.append(Text(type='reference', text='REF**', at=[rm/2, t_slk-txt_offset], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text=footprint_name, at=[rm/2, h_slk/2+txt_offset], layer='F.Fab'))

        # create FAB-layer
        kicad_mod.append(RectLine(start=[left, top], end=[left+w, top+h], layer='F.Fab', width=lw_fab))

        # create SILKSCREEN-layer
        kicad_mod.append(RectLine(start=[l_slk, t_slk], end=[l_slk+w_slk, t_slk+h_slk], layer='F.SilkS'))
        kicad_mod.append(Line(start=[xl1_slk, t_slk], end=[xl1_slk, t_slk+h_slk], layer='F.SilkS'))
        kicad_mod.append(Line(start=[xl2_slk, t_slk], end=[xl2_slk, t_slk+h_slk], layer='F.SilkS'))

        # create courtyard
        kicad_mod.append(RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt+w_crt), roundCrt(t_crt+h_crt)], layer='F.CrtYd', width=lw_crt))

        # create pads 
        kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[0, 0], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))
        kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[rm, 0], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))

        # add model
        if (has3d!=0):
            kicad_mod.append(Model(filename=lib_name + ".3dshapes/"+footprint_name+".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))

        # print render tree
        # print(kicad_mod.getRenderTree())
        # print(kicad_mod.getCompleteRenderTree())

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile(footprint_name+'.kicad_mod')


def makeRES_VERTRSIMPLE(rm, rmdisp, rl, rw, rh, ddrill, footprint_namepart, description, tags, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0):
        padx=2*ddrill
        pady=padx
        if (largepadsx):
            padx=max(padx, largepadsx)
        if (largepadsy):
            pady=max(pady, largepadsy)
        crt_offset=0.25
        slk_offset=0.15
        lw_fab=0.1
        lw_crt=0.05
        lw_slk=0.15
        txt_offset=1

        d=max(rw,rh)
        left=-d/2
        top=-d/2
        d_slk=d+2*slk_offset
        w_slk=rm+d/2+padx/2+2*slk_offset
        l_slk=left-slk_offset
        r_slk=l_slk+w_slk
        t_slk=-d_slk/2
        xl1_slk=left+(rw-rh)/2
        xl2_slk=xl1_slk+rh
        w_crt=w_slk+2*crt_offset
        h_crt=d_slk+2*crt_offset
        l_crt=l_slk-crt_offset
        t_crt=t_slk-crt_offset
        
        
        lib_name = "Resistors_ThroughHole"
        footprint_name="Resistor{0}_RM{1}mm".format(footprint_namepart,rmdisp)
        if (specialfpname!=""):
            footprint_name=specialfpname;
        print(footprint_name)

        # init kicad footprint
        kicad_mod = Footprint(footprint_name)
        kicad_mod.setDescription(description)
        kicad_mod.setTags(tags)

        # set general values
        kicad_mod.append(Text(type='reference', text='REF**', at=[rm/2, t_slk-txt_offset], layer='F.SilkS'))
        kicad_mod.append(Text(type='value', text=footprint_name, at=[rm/2, d_slk/2+txt_offset], layer='F.Fab'))

        # create FAB-layer
        kicad_mod.append(Circle(center=[0, 0], radius=d/2, layer='F.Fab', width=lw_fab))

        # create SILKSCREEN-layer
        kicad_mod.append(Circle(center=[0, 0], radius=d_slk/2, layer='F.SilkS'))
        kicad_mod.append(Line(start=[d_slk/2, 0], end=[rm-padx/2-0.3, 0], layer='F.SilkS'))

        # create courtyard
        kicad_mod.append(RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt+w_crt), roundCrt(t_crt+h_crt)], layer='F.CrtYd', width=lw_crt))

        # create pads 
        kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[0, 0], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))
        kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[rm, 0], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))

        # add model
        if (has3d!=0):
            kicad_mod.append(Model(filename=lib_name + ".3dshapes/"+footprint_name+".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))

        # print render tree
        # print(kicad_mod.getRenderTree())
        # print(kicad_mod.getCompleteRenderTree())

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile(footprint_name+'.kicad_mod')

if __name__ == '__main__':
    makeRES(25.4,  25, 19, 8,  8,    1, "_Ceramic_Horizontal", "Resistor, Ceramic, Horizontal", "R Resistor Ceramic Horizontal", [0.5, 0, 0], [4, 4, 4 ])
    makeRES(30.48, 30, 23, 9,  9,  1.2, "_Ceramic_Horizontal", "Resistor, Ceramic, Horizontal", "R Resistor Ceramic Horizontal", [0.6, 0, 0], [4, 4, 4 ])
    makeRES(45.72, 45, 36, 11, 10, 1.2, "_Ceramic_Horizontal", "Resistor, Ceramic, Horizontal", "R Resistor Ceramic Horizontal", [0.9, 0, 0], [4, 4, 4 ])
    makeRES(60.96, 60, 50, 14, 13, 1.2, "_Ceramic_Horizontal", "Resistor, Ceramic, Horizontal", "R Resistor Ceramic Horizontal", [1.2, 0, 0], [4, 4, 4 ])
    makeRES(80.01, 80, 65, 16, 15, 1.2, "_Ceramic_Horizontal", "Resistor, Ceramic, Horizontal", "R Resistor Ceramic Horizontal", [1.58, 0, 0], [3.95, 4, 4 ])
    makeRES(35.0012, 35, 20, 6.6, 6.6, 1.2, "_Ceramic_Horizontal", "Resistor, Cement, Horizontal, Meggit, SBC, SBC-2,", "R Resistor Cement Horizontal Meggit SBC SBC-2 ", [1.58, 0, 0], [3.95, 4, 4 ], 0, "Resistor_Cement_Horizontal_Meggitt-SBC-2")
    makeRES_VERT(5, 5, 0, 14, 10, 1.2, "_Ceramic_Vertical", "Resistor, Cement, Vertical, 5W, 7W, Meggitt, KOA, BSR, BGR, BWR, 5N, 7N,", "R Resistor Cement Vertical 5W 7W Meggitt KOA BSR BGR BWR 5N 7N ", [1.58, 0, 0], [3.95, 4, 4 ], 0, "Resistor_Cement_Vertical_KOA-BGR-5N-7N")
    makeRES_VERT(5, 5, 0, 14, 10, 1.2, "_Ceramic_Vertical", "Resistor, Cement, Vertical, 5W, 7W, Meggitt, KOA, BSR, BGR, BWR, 5N, 7N,", "R Resistor Cement Vertical 5W 7W Meggitt KOA BSR BGR BWR 5N 7N ", [1.58, 0, 0], [3.95, 4, 4 ], 0, "Resistor_Cement_Vertical_LargePads_KOA-BGR-5N-7N", 3)
    makeRES_VERT(5, 5, 0, 13, 9, 1.2, "_Ceramic_Vertical", "Resistor, Cement, Vertical, 3W, Meggitt, KOA, BSR, BGR, BWR, 3N,", "R Resistor Cement Vertical 3W Meggitt KOA BSR BGR BWR 3N ", [1.58, 0, 0], [3.95, 4, 4 ], 0, "Resistor_Cement_KOA-BGR-3N")
    makeRES_VERT(5, 5, 0, 13, 9, 1.2, "_Ceramic_Vertical", "Resistor, Cement, Vertical, 3W, Meggitt, KOA, BSR, BGR, BWR, 3N,", "R Resistor Cement Vertical 3W Meggitt KOA BSR BGR BWR 3N ", [1.58, 0, 0], [3.95, 4, 4 ], 0, "Resistor_Cement_LargePads_KOA-BGR-3N", 3)
    makeRES_SIMPLE(7.62,   7, 3.4, 1.7, 1.7, 1, "_Horizontal", "Resistor, Axial,  RM 7.62mm, 1/8W,", "Resistor Axial RM 7.62mm 1/8W", [0.5, 0, 0], [4, 4, 4 ], 0)
    makeRES_SIMPLE(10.16, 10, 6.5, 2.3, 2.3, 1, "_Horizontal", "Resistor, Axial,  RM 10.16mm, 1/4W,", "Resistor Axial RM 10.16mm 1/4W", [0.2, 0, 0], [0.4, 0.4, 0.4 ], 1)
    makeRES_SIMPLE(15, 15, 6.5, 2.3, 1.7, 1, "_Horizontal", "Resistor, Axial,  RM 15mm, 1/4W,", "Resistor Axial RM 15mm 1/4W", [0.295, 0, 0], [0.395, 0.4, 0.4 ], 1)
    makeRES_SIMPLE(20, 20, 6.5, 2.3, 1.7, 1, "_Horizontal", "Resistor, Axial,  RM 20mm, 1/4W,", "Resistor Axial RM 20mm 1/4W", [0.395, 0, 0], [0.395, 0.4, 0.4 ], 1)
    makeRES_SIMPLE(25, 25, 17, 6, 1.7, 1, "_Horizontal", "Resistor, Axial,  RM 25mm, 3W,", "Resistor Axial RM 25mm 3W", [0.395, 0, 0], [0.395, 0.4, 0.4 ], 0)
    makeRES_SIMPLE(30, 30, 24, 8, 1.7, 1.2, "_Horizontal", "Resistor, Axial,  RM 30mm, 5W,", "Resistor Axial RM 30mm 5W", [0.395, 0, 0], [0.395, 0.4, 0.4 ], 0)
    makeRES_VERTRSIMPLE(5.08, 5, 15, 5, 5, 1, "_Vertical", "Resistor, Axial,  RM 5.08mm, 2W,", "Resistor Vertical RM 5.08mm 2W", [0.2, 0, 0], [0.4, 0.4, 0.4 ], 0)
    makeRES_VERTRSIMPLE(7.5, 7.5, 24, 10, 10, 1, "_Vertical", "Resistor, Axial,  RM 7.62mm, 5W,", "Resistor Vertical RM 7.62mm 5W", [0.2, 0, 0], [0.4, 0.4, 0.4 ], 0)
