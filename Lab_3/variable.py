
class Variable:
    def __init__(self, domain, assigned=False):
        self.domain = domain
        self.assigned = assigned

    def set_domain(self, one_var_domain):
        self.domain = one_var_domain
        self.assigned = True
