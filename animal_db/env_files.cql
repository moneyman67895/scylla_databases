create table duwc_rank_kingdom( kingdom text, phyllum text, class text, order text, family text, genus text, species text, 
create type rank_ingdom(scientific_name
create type range_frequency(min_val float, max_val_float
create type rank_phyllum(scientific_name text, common_description text, number_of_species int, descriptor_size range_frequency

