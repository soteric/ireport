class V1Defect():
    def __init__(self, v1_id='', oid='', title='', owner='', sprint='', module='', custom_status='', status='', sla='', type='', configType=''):
        self.id = v1_id
        self.oid = oid
        self.title = title
        self.owner = owner
        self.custom_status = custom_status
        self.module = module
        self.sprint = sprint
        self.status = status
        self.sla = sla
        self.type = type
        self.configType = configType