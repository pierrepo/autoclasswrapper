import autoclasswrapper as wrapper

results = wrapper.Output()
results.extract_results()
results.aggregate_input_data()
results.write_cdt()
results.write_cdt(with_proba=True)
results.write_cluster_stats()
results.write_dendrogram()
results.wrap_outputs()
