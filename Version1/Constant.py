#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年9月7日
@author: Irony
@site: https://github.com/892768447
@email: 892768447@qq.com
@file: Constant
@description: 
"""
import json


__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class Result:

    def __init__(self, message):
        '''
        :param message: json字符串结果
        '''
        try:
            self._message = message if isinstance(
                message, dict) else json.loads(message)
        except:
            self._message = {}
        self.ret = self._message.get('ret', 0)                   # 状态码
        self.msg = self._message.get('msg', 0)                   # 错误消息
        self.id = self._message.get('id', 0)                     # 文档ID
        self.dpi = self._message.get('dpi', 0)                   # 图片dpi
        self.width = self._message.get('width', 0)               # 图片宽度
        self.height = self._message.get('height', 0)             # 图片高度
        self.saved = self._message.get('saved', True)            # 图片是否保存
        self.method = self._message.get('method', 'callback')    # 回调函数名
        self.params = self._message.get('params', [])            # 回调函数参数

    def __str__(self):
        return str(self._message)


class Message:

    def __init__(self, tid, ctype, data):
        '''
        :param tid:   传输id
        :param ctype: 内容类型
        :param data:  内容
        '''
        self.tid = tid
        self.ctype = ctype
        self.data = data

    def isImg(self):
        return self.ctype == 3

    def toDict(self):
        if self.isImg():
            return {}
        return Result(self.data.decode())

    def __str__(self):
        return '[tid: {}, type: {}, isImage: {}, data len: {}]'.format(
            self.tid, self.ctype, self.isImg(), len(self.data))


# 打开图片
CodeOpenImage = """#target photoshop
cTID = function(s) {{ return app.charIDToTypeID(s); }};
sTID = function(s) {{ return app.stringIDToTypeID(s); }};

function convert() {{
    // convert color profile
    var idconvertToProfile = stringIDToTypeID( "convertToProfile" );
    var desc20 = new ActionDescriptor();
    var idnull = charIDToTypeID( "null" );
    var ref1 = new ActionReference();
    var idDcmn = charIDToTypeID( "Dcmn" );
    var idOrdn = charIDToTypeID( "Ordn" );
    var idTrgt = charIDToTypeID( "Trgt" );
    ref1.putEnumerated( idDcmn, idOrdn, idTrgt );
    desc20.putReference( idnull, ref1 );
    var idTMd = charIDToTypeID( "TMd " );
    var idRGBM = charIDToTypeID( "RGBM" );
    desc20.putClass( idTMd, idRGBM );
    var idEngn = charIDToTypeID( "Engn" );
    desc20.putString( idEngn, "Microsoft ICM" );
    var idInte = charIDToTypeID( "Inte" );
    var idInte = charIDToTypeID( "Inte" );
    var idImg = charIDToTypeID( "Img " );
    desc20.putEnumerated( idInte, idInte, idImg );
    var idMpBl = charIDToTypeID( "MpBl" );
    desc20.putBoolean( idMpBl, true );
    var idDthr = charIDToTypeID( "Dthr" );
    desc20.putBoolean( idDthr, true );
    var idFltt = charIDToTypeID( "Fltt" );
    desc20.putBoolean( idFltt, false );
    var idrasterizePlaced = stringIDToTypeID( "rasterizePlaced" );
    desc20.putBoolean( idrasterizePlaced, false );
    var idsdwM = charIDToTypeID( "sdwM" );
    desc20.putInteger( idsdwM, -1 );
    executeAction( idconvertToProfile, desc20, DialogModes.NO );
}}

function main() {{
    //open image
    var desc1=new ActionDescriptor();
    try {{
        desc1.putPath(cTID('null'), new File("{0}"));
        executeAction(sTID('open'), desc1, DialogModes.NO);
    }} catch (e) {{
        desc1.putPath(cTID('null'), new File(File.encode("{0}")));
        executeAction(sTID('open'), desc1, DialogModes.NO);
    }}
    //convert png to background layer
    if (app.activeDocument.activeLayer.isBackgroundLayer !== true) {{
        var idMk = charIDToTypeID( "Mk  " );
        var desc403 = new ActionDescriptor();
        var idnull = charIDToTypeID( "null" );
        var ref102 = new ActionReference();
        var idBckL = charIDToTypeID( "BckL" );
        ref102.putClass( idBckL );
        desc403.putReference( idnull, ref102 );
        var idUsng = charIDToTypeID( "Usng" );
        var ref103 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idTrgt = charIDToTypeID( "Trgt" );
        ref103.putEnumerated( idLyr, idOrdn, idTrgt );
        desc403.putReference( idUsng, ref103 );
        executeAction( idMk, desc403, DialogModes.NO );
    }}
    //convert color profile
    try {{
        var propId = sTID("profile");
        var ref = new ActionReference();
        ref.putProperty(cTID("Prpr"), propId);
        ref.putEnumerated(cTID("Dcmn"), cTID("Ordn"), cTID("Trgt"));
        var desc = app.executeActionGet(ref);
        var ret = desc.getString(propId);
        if (ret !== "sRGB IEC61966-2.1") {{
            convert();
        }}
    }} catch (e) {{
        // force convert
        try {{
            convert();
        }} catch(ee) {{
        }}
    }}
}}

try {{
    main();
    '{{"ret":0,"msg":"","id":'+app.activeDocument.id+',"dpi":'+app.activeDocument.resolution+',"width":'+parseInt(app.activeDocument.width)+',"height":'+parseInt(app.activeDocument.height)+',"saved":'+app.activeDocument.saved+',"method":"callback","params":[]}}'
}} catch (e) {{
    '{{"ret":-1,"msg":"'+e+'","id":0,"dpi":0,"width":0,"height":0,"saved":true,"method":"callback","params":[]}}'
}}
"""

# 获取图片
CodeGetImage = """#target photoshop
var idNS = stringIDToTypeID( "sendDocumentThumbnailToNetworkClient" );
var desc1 = new ActionDescriptor();
var documentID = {};
if (documentID !== -1) {{
    //get image by document id
    desc1.putInteger( stringIDToTypeID( "documentID" ), documentID );
}}
desc1.putInteger( stringIDToTypeID( "width" ), {} );
desc1.putInteger( stringIDToTypeID( "height" ), {} );
desc1.putInteger( stringIDToTypeID( "format" ), "1" );
executeAction( idNS, desc1, DialogModes.NO );
"""
