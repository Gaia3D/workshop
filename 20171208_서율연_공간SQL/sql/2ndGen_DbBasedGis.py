#-*- coding: utf-8 -*-
import timeit
from qgis.analysis import QgsGeometryAnalyzer

# 캔버스 초기화
QgsMapLayerRegistry.instance().removeAllMapLayers()

# DB 접속정보
uri = QgsDataSourceURI()
uri.setConnection("localhost", "5432", "foss4g", "postgres", "postgres")

start = timeit.default_timer()
pre = start

# 도로 레이어 불러
uri.setDataSource("public", "road_link2", "geom")
roadLayer = iface.addVectorLayer(uri.uri(False), "road", "postgres")

crr = timeit.default_timer()
print (u"도로 읽기 : {}ms".format(int((crr - pre)*1000)))
pre = crr

# 8차선 이상 선택하여
expr = QgsExpression( "\"LANES\">=8" )
it = roadLayer.getFeatures( QgsFeatureRequest( expr ) )
ids = [i.id() for i in it]
roadLayer.setSelectedFeatures( ids )

crr = timeit.default_timer()
print (u"8차선 이상 필터링 : {}ms".format(int((crr - pre)*1000)))
pre = crr

# 500 미터 버퍼  생성 후
QgsGeometryAnalyzer().buffer(roadLayer, "/Data/buffer500.shp", 500, True, True, -1)
crr = timeit.default_timer()
print (u"500 미터 버퍼 생성: {}ms".format(int((crr - pre)*1000)))
pre = crr

bufferLayer = iface.addVectorLayer("/Data/buffer500.shp", "buffer500", "ogr")

feats = [ feat for feat in bufferLayer.getFeatures() ]
geom_buffer = feats[0].geometry()

crr = timeit.default_timer()
print (u"버퍼 파일 읽기 : {}ms".format(int((crr - pre)*1000)))
pre = crr

# 지하철역 불러
uri.setDataSource("public", "subway_station", "geom")
stationLayer = iface.addVectorLayer(uri.uri(False), "road", "postgres")

crr = timeit.default_timer()
print (u"지하철역 읽기 : {}ms".format(int((crr - pre)*1000)))
pre = crr

# 버퍼 안에 들어가는 것 선택 후
selectedStation = [feature.id() for feature in stationLayer.getFeatures()
    if feature.geometry().within(geom_buffer) ]

crr = timeit.default_timer()
print (u"버퍼 안의 지하철역 필터링 : {}ms".format(int((crr - pre)*1000)))
pre = crr

# 결과 파일로 저장
stationLayer.setSelectedFeatures( selectedStation )
QgsVectorFileWriter.writeAsVectorFormat( stationLayer, "/Data/Result.shp", "cp949", stationLayer.crs(), "ESRI Shapefile", 1)
iface.addVectorLayer("/Data/Result.shp", "result", "ogr")

crr = timeit.default_timer()
print (u"결과 파일 저장 : {}ms".format(int((crr - pre)*1000)))

print (u"========================")
print (u"전체 수행시간 : {}ms".format(int((crr - start)*1000)))
