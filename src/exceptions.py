class RunCoccinelleError(Exception):
    pass

class SPatchVersionError(Exception):
    def __init__(self, required_version, installed_version):      
        if installed_version is not None:    
            message = f"Version {required_version} of Coccinelle (SPatch) should be installed, but {installed_version} is installed instead"
        else:
            message = f"Version {required_version} of Coccinelle (SPatch) should be installed, but Coccinelle not installed"
        super().__init__(message)
