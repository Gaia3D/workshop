select * from subway_station
where gid in
(
	select distinct st.gid
	from subway_station as st, road_link2 as road
	where road.lanes >= 8
	  and ST_Distance(st.geom, road.geom) <= 500
)
