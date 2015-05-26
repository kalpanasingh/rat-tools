{
name: "GEO",
index: "world",
run_range: [0, 0],
pass: 0,
enable: 1,
invisible: 1, // omitted for visualization

mother: "", // world volume has no mother

factory: "solid",
solid: "box",

half_size: [200000.0, 200000.0, 200000.0], // mm

material: "rock",
color: [0.67, 0.29, 0.0],
}

{
name: "GEO",
index: "h2o",
run_range: [0, 0],
pass: 0,
enable: 1,
invisible: 1, // omitted for visualization

mother: "world",

factory: "solid",
solid: "box",

half_size: [190000.0, 190000.0, 190000.0], // mm

material: "lightwater_sno",
color: [0.67, 0.29, 0.0],
}

{
name: "GEO",
index: "innerPMT",
run_range: [0, 0],
pass: 0,
enable: 1,

mother: "h2o",

factory: "pmtbuilder",

pmt_build_type: [1], // NORMAL
pmt_type: ["r1408"],

add_concentrator: [1],
concentrator_type: ["cRAT"],

add_bucket: [1],
bucket_type: ["bRAT"],

add_pmtbase: [0],
pmtbase_type: ["r1408"],

grey_disc: [0],
grey_disc_model_params: ["DiscOptics0_0"],

sensitive_detector: "/mydet/pmt/inner",

vis_simple: 1,
vis_invisible: 1,
}
