class Problem(object):

    def fitness(self, phenotype):
        '''
        Returns a float between 0 and 1, 1 is optimal solution
        '''
        raise NotImplementedError("Must be implemented by Problem subclass.")

    def create_initial_population(self, population_size):
        '''
        Returns an iterable of Individuals
        '''
        raise NotImplementedError("Must be implemented by Problem subclass.")

    def geno_to_pheno(self, genotype):
        '''
        Converts a genotype to a phenotype
        '''
        raise NotImplementedError("Must be implemented by Problem subclass.")

    def mutate_genome_component(self, component):
        '''
        Mutates a single genome component
        '''
        raise NotImplementedError("Must be implemented by Problem subclass.")

    def pre_generation_hook(self):
        '''
        Function that is called after each generation
        '''
        pass

    def generate_new_scenario(self):
        raise NotImplementedError("Must be implemented by Problem subclass.")

    def __repr__(self):
        return self.__class__.__name__

    def visualization(self, *args, **kwargs):
        pass
