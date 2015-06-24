// This geometry is for SPECTRE with the Y90 capillary. 

{
type: "GEO",
version: 1,
index: "world",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "",
enable: 1,

factory: "solid",
solid: "box",

half_size: [950.0, 950.0, 455.0],
position: [0.0, 0.0, 0.0],
rotation: [0.0, 0.0, 0.0],
material: "air",
}

{
type: "GEO",
version: 1,
index: "acrylic",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "world",
enable: 1,

factory: "solid",
solid: "sphere",

r_max: 203.2,

position: [0.0, 0.0,-251.7],
material: "acrylic_uva_McMaster",
}

{
type: "GEO",
version: 1,
index: "scint",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "acrylic",
enable: 1,

factory: "solid",
solid: "sphere",

r_max: 201.7,

material: "labppo_scintillator",
}

{
type: "GEO",
version: 1,
index: "aluminum_disc",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "scint",
enable: 1,

factory: "solid",
solid: "tube",

r_max: 66.7,
half_z: 0.1,

position: [0.0, 0.0 ,190.15],
material: "aluminum",
}



{
type: "GEO",
version: 1,
index: "source_leg_1",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "scint",
enable: 1,

factory: "solid",
solid: "tube",

r_max: 2.5,
half_z:67.5,

position: [0.0, 21.25 ,122.55],
material: "ABSplastic",
}

{
type: "GEO",
version: 1,
index: "source_leg_2",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "scint",
enable: 1,

factory: "solid",
solid: "tube",

r_max: 2.5,
half_z:67.5,

position: [-18.403, -10.625 ,122.55],
material: "ABSplastic",
}

{
type: "GEO",
version: 1,
index: "source_leg_3",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "scint",
enable: 1,

factory: "solid",
solid: "tube",

r_max: 2.5,
half_z:67.5,

position: [18.403, -10.625 ,122.55],
material: "ABSplastic",
}

{
type: "GEO",
version: 1,
index: "acrylic_center_disc",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "scint",
enable: 1,

factory: "solid",
solid: "tube",

r_max: 22.5,
half_z:1.25,

position: [0.0, 0.0 ,53.8],
material: "acrylic_uva_McMaster",
}

{
type: "GEO",
version: 1,
index: "acrylic_capholder_disc",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "scint",
enable: 1,

factory: "solid",
solid: "tube",

r_max: 15.0,
half_z:7.5,

position: [0.0, 0.0 ,62.55],
material: "acrylic_uva_McMaster",
}

{
type: "GEO",
version: 1,
index: "acrylic_capholder_disc_lower",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "scint",
enable: 1,

factory: "solid",
solid: "tube",

r_max: 15.0,
half_z:10.0,

position: [0.0, 0.0 ,42.55],
material: "acrylic_uva_McMaster",
}

{
type: "GEO",
version: 1,
index: "capillary",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "scint",
enable: 1,

factory: "solid",
solid: "tube",

r_max: 0.55,
half_z:21.25,

position: [0.0, 0.0 ,11.30],
material: "glass",
}

{
type: "GEO",
version: 1,
index: "capillary_airgap",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "capillary",
enable: 1,

factory: "solid",
solid: "tube",

r_max: 0.45,
half_z:21.225,

position: [0.0, 0.0 ,0.0],
material: "air",
}

{
type: "GEO",
version: 1,
index: "source_droplet",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "capillary_airgap",
enable: 1,

factory: "solid",
solid: "tube",

r_max: 0.45,
half_z:3.0,

position: [0.0, 0.0 ,0.0],
material: "lightwater_sno",
}

{
type: "GEO",
version: 1,
index: "triggerPMT",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "world",
enable: 1,

factory: "pmtbuilder",

pmt_build_type: [2], // trigger
pmt_type: ["r7081"],

add_concentrator: [0],
concentrator_type: ["cRAT"],

add_bucket: [0],
bucket_type: ["bRAT"],

add_pmtbase: [0],
pmtbase_type: ["r1408"],

grey_disc: [0],
grey_disc_model_params: ["DiscOptics0_0"],

sensitive_detector: "/mydet/pmt/inner",

vis_simple: 1,
vis_invisible: 0,
}

{
type: "GEO",
version: 1,
index: "innerPMT",
run_range: [0, 0],
pass: 0,
timestamp: "",
comment: "",
production: false,
mother: "world",
enable: 1,

factory: "pmtbuilder",

pmt_build_type: [1], // Data PMTs
pmt_type: ["r11780-HQE"],

add_concentrator: [0],
concentrator_type: ["cRAT"],

add_bucket: [0],
bucket_type: ["bRAT"],

add_pmtbase: [0],
pmtbase_type: ["r1408"],

grey_disc: [0],
grey_disc_model_params: ["DiscOptics0_0"],

sensitive_detector: "/mydet/pmt/inner",

vis_simple: 1,
vis_invisible: 0,
}
