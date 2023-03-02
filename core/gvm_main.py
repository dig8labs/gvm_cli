"""
Author: QuantumCore
"""
from gvm.protocols.gmp import Gmp
from gvm.connections import SSHConnection
from gvmtools.helper import Table
import colorama
from colorama import Fore, Style

colorama.init()

# just for this script
good = "[" + Style.RESET_ALL+Style.BRIGHT+Fore.GREEN + "+" + Style.RESET_ALL + "]"
bad = "[" + Style.RESET_ALL

"""
Port Lists
all-iana-assigned-tcp-33d0cd82-57c6-11e1-8ed1-406186ea4fc5.xml
all-iana-assigned-tcp-and-udp-4a4717fe-57d2-11e1-9a26-406186ea4fc5.xml
all-tcp-and-nmap-top-100-udp-730ef368-57e2-11e1-a90f-406186ea4fc5.xml
"""
class GVM_MAIN:
    def __init__(self, gmp_conn):
        self.gmp_conn = gmp_conn

    TASKS = []
   # If these are different in your gvm,
	# Open issue, this is a simple fix
    PORT_LIST = [
        "all-iana-assigned-tcp=33d0cd82-57c6-11e1-8ed1-406186ea4fc5", # all-iana-assigned-tcp
        "all-iana-assigned-tcp-and-udp=4a4717fe-57d2-11e1-9a26-406186ea4fc5", # all-iana-assigned-tcp-and-udp
        "all-tcp-and-nmap-top-100-udp=730ef368-57e2-11e1-a90f-406186ea4fc5", # all-tcp-and-nmap-top-100-udp
    ]

    full_and_fast_scan_config_id = 'daba56c8-73ec-11df-a475-002264764cea'
    openvas_scanner_id = '08b69003-5fc2-4037-a479-93b440211c73'

    
    def portList(self, i):
        return self.PORT_LIST[i]

    def create_task(self, name, target_id):
        """
        Create a Task
        name - Scan name
        target_id - Target ID
        scan_config_id - Scan configuration ID
        scanner_id - scanner ID
        """
        try:
            response = self.gmp_conn.create_task(
                name=name,
                config_id=self.full_and_fast_scan_config_id,
                target_id=target_id,
                scanner_id=self.openvas_scanner_id,
            )
            return response.get('id')
        except Exception as E:
            print(bad, "Error : " + str(E))
    

    def start_task(self, task_id):
        """
        Start a Task
        - task_id - Task ID
        """
        try:
            response = self.gmp_conn.start_task(task_id)
            
            # the response is
            # <start_task_response><report_id>id</report_id></start_task_response>
            return response[0].text
        except Exception as E:
            print(bad, "Error : " + str(E))
    
    def create_target(self, ipaddress, name, port_list_id):
    
        try:
            # create a unique name by adding the current datetime
            #name = f"Scan for {ipaddress} {str(datetime.datetime.now())}"
            response = self.gmp_conn.create_target(
                name=name, hosts=[ipaddress], port_list_id=port_list_id
            )
            return response.get('id')
        except Exception as E:
            print(bad, "Error : " + str(E))
          

    def ListTasks(self):
        response_xml = self.gmp_conn.get_tasks()
        tasks_xml = response_xml.xpath('task')
        heading = ['ID', 'Name', 'Severity', 'REPORT ID', 'Status']
        rows = []
        for task in tasks_xml:
            #pretty_print(task)
            name = ''.join(task.xpath('name/text()'))
            task_id = task.get('id')
            severity = ''.join(task.xpath('last_report/report/severity/text()'))
            status = ''.join(task.xpath('status/text()'))
            
            last_report = task.find('last_report')
            if last_report is not None:
                report = last_report.find('report')
                if report is not None:
                    report_id = report.get('id')
            else:
                report_id = "n/a"
            rows.append([task_id, name, severity, report_id, status])
            self.TASKS.append(task_id)

        print(Table(heading=heading, rows=rows))
        print(good, " {} tasks found.".format(len(self.TASKS)))
        self.TASKS.clear()

    def ListTargets(self):

        heading = ['ID', 'Name', 'IP/Host', 'Port List']
        rows = []
        response_xml = self.gmp_conn.get_targets()
        target_xml = response_xml.xpath('target')
        for target in target_xml:
            name = ''.join(target.xpath('name/text()'))
            target_id = target.get('id')
            host = ''.join(target.xpath('hosts/text()'))
            plist = target.find('port_list')
            port = plist.get('id')
            
            rows.append([target_id, name, host, port])

        print(Table(heading=heading, rows=rows))
