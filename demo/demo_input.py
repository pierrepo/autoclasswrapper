import autoclasswrapper as wrapper

# create object to prepare dataset
clust = wrapper.Input()

# load dataset in tsv format
clust.add_input_data("sample-3-classes-real-location.tsv", "real location", 0.01)

# merge datasets if multiple dataset had been loaded
clust.merge_dataframes()

# create files needed by autoclass
clust.create_db2_file()
clust.create_hd2_file()
clust.create_model_file()
clust.create_sparams_file()
clust.create_rparams_file()
