from DAO.Db.DbConnect import DbConnect


class ReportFactory():

    _register = {}

    @classmethod                                                                                                                                              
    def register(cls, name: str):                                                                                                                             
        def decorator(subclass):                                                                                                                              
            cls._register[name] = subclass                                                                                                                    
            return subclass                                                                                                                                   
        return decorator                                                                                                                                      


    @classmethod                                                                                                                                              
    def create_report(cls, db: DbConnect, name: str, config: dict):                                                                                                         
        report_class = cls._register.get(name)                                                                                                               
        if not report_class:                                                                                                                                 
            raise ValueError(f"Отчёт {name} не найден")     
                                                                                                      
        return report_class(db, config)
    
import Service.Reports.CreateReconciliationPassagersReport
