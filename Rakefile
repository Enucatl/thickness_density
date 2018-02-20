require "csv"

datasets = CSV.table "datasets.csv"

datasets.each do |dataset|

  desc "calculate thickness and density of #{dataset[:name]}"
  file dataset[:thickness_density] => ["thickness_density.py", dataset[:folder], dataset[:height_map_left], dataset[:height_map_right]] do |f|
    sh "python #{f.prerequisites[0]} #{f.prerequisites[1]} #{f.name} --height_map_left #{f.prerequisites[2]} --height_map_right #{f.prerequisites[3]}"
  end

  desc "calculate dfec of #{dataset[:name]}"
  file dataset[:dfec] => ["#{ENV['HOME']}/code/compare-lungs-theory/build_dfec_structure_factor.py", dataset[:thickness_density]] do |f|
    sh "python #{f.prerequisites[0]} --output #{f.name} --sampling 512 --sphere_density 1.8 --volume_fraction $(sed -n 2p #{dataset[:thickness_density]} | cut -d ',' -f 3)"
  end

end

desc "calculate all dfec"
task :dfec => datasets[:dfec]

desc "calculate all thicknesses"
task :thicknesses => datasets[:thickness_density]
