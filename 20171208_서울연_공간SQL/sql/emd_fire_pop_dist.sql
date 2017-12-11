SELECT 
  min_t.emd_cd, emd_nm, pop, fire_nm, dt.dist, 
  pop*dt.dist as pop_dist
FROM
(
  SELECT 
    emd.emd_cd,
    min(ST_Distance(ST_Centroid(emd.geom), fire.geom)) AS dist
  FROM 
    admin_emd AS emd, firestation AS fire
  GROUP BY emd_cd
) AS min_t,
(
  SELECT 
    emd.emd_cd, 
    emd.emd_nm, 
    emd.pop2008 as pop, 
    fire.nam as fire_nm, 
    ST_Distance(ST_Centroid(emd.geom), fire.geom) AS dist
  FROM 
    admin_emd AS emd, firestation AS fire
) AS dt
WHERE
  min_t.emd_cd = dt.emd_cd AND min_t.dist = dt.dist
ORDER BY pop_dist
LIMIT 20;