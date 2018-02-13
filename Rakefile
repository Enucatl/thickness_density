require "csv"

datasets = CSV.table "datasets.csv"

datasets.each do |dataset|

  desc "calculate thickness and density of #{dataset[:name]}"
  file dataset[:thickness_density] => ["thickness_density.py", dataset[:folder], dataset[:height_map_left], dataset[:height_map_right]] do |f|
    sh "python #{f.prerequisites[0]} #{f.prerequisites[1]} #{f.name} --height_map_left #{f.prerequisites[2]} --height_map_right #{f.prerequisites[3]}"
  end

end

desc "calculate all thicknesses"
task :all => datasets[:thickness_density]
