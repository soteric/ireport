class V1Story():
    def __init__(self, v1_id='', oid='', title='', sprint='', module='', custom_status='', status=''):
        self.id = v1_id
        self.oid = oid
        self.title = title
        self.custom_status = custom_status
        self.module = module
        self.sprint = sprint
        self.status = status