import autoclasswrapper as wrapper

# search autoclass in path
wrapper.search_autoclass_in_path()

# create object to run autoclass
run = wrapper.Run()

# prepare script to run autoclass
run.create_run_file()

# run autoclass
run.run()
