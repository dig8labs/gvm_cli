"""
This is a Command line GVM Controller
Author: QuantumCore
"""

import configparser
from lxml import etree
from core.gvm_main import *
from gvm.transforms import EtreeTransform

settings = configparser.ConfigParser()

try:
    settings.read("settings.ini")
    config = settings['DEFAULT']
except Exception as e:
    print(str(e))
    exit(1)


def main():


    try:
        connection = SSHConnection(hostname=config['host'],username=config['ssh_user'],password=config['ssh_pass'])
        print("[^] Connecting to {u}@{h} ...".format(u =config['ssh_user'], h = config['host']))
        transform = EtreeTransform()
        with Gmp(connection, transform=transform) as gmp:
            try:
                print(good, "Connected.")
                print("[^] Authenticating to GVM with user {}...".format(config['gvm_user']))
                gmp.authenticate(config['gvm_user'], config['gvm_pass'])
                g = GVM_MAIN(gmp)

                def targetCreator(g):
                    name = input("[^] Target Name : ")
                    to_scan = input("[^] Enter Target IP / HOST : ")
                    if(len(to_scan) > 0 and len(name) > 0):
                        for pl in g.PORT_LIST:
                            print( str(g.PORT_LIST.index(pl)) + " -> " + pl)
                        pl_ask = input("[^] Enter Index of Port List to Use : ")
                        print(good, " Using Port List : " + g.portList(int(pl_ask)).split("=")[0] + "-" + g.portList(int(pl_ask)).split("=")[1])
                        print(good, " Creating Target...")
                        target_id = g.create_target(to_scan, name, g.portList(int(pl_ask)).split("=")[1])
                        print(good, " Target created with ID : " + target_id)

                try:
                    while(True):
                        try:
                            cmd = input(Style.BRIGHT + Fore.GREEN + "GVM"+ Style.RESET_ALL + "({u}@{h})> ".format(u =config['ssh_user'], h = config['host']))
                            if(cmd == "help"):
                                print("""
                                - list_tasks - List all Tasks
                                - del_task - Delete a Task
                                - create_task - Create a Task
                                - start_task - Start a Task
                                - create_target - Create a Target
                                - list_targets - List all Targets
                                - del_target - Delete a Target
                                - task_details - Get Details on a Task
                                - get_report - Get Report on a Task

                                ~ QuantumCore
                                """)

                            elif(cmd == "get_report"):
                                fl = input("[^] Filename to save as (XML) : ")
                                report_id = input("[^] Report ID : ")
                                if(len(report_id) > 0 and len(fl) > 0):
                                    report = gmp.get_report(report_id)
                                    rp = etree.ElementTree(report)
                                    rp.write(fl, pretty_print=True)


                            elif(cmd == "create_task"):
                                scfg = ""
                                name = input("[^] Scan Name : " )
                                target_id = input("[^] Target ID : ")
                                task_id = g.create_task(
                                    name,
                                    target_id
                                )
                                print("[+] Task created with ID " + task_id)

                                start = input("[^] Do you want to start now? (y/N) : ")
                                if(start.startswith("y")):
                                    g.start_task(task_id)
                                    
                                
                            elif(cmd == "list_tasks"):
                                g.ListTasks()
                            
                            elif(cmd.startswith("del_task")):
                                taskid = input("[^] Task ID : ")
                                if(len(taskid) > 0):
                                    delete = gmp.delete_task(taskid)
                                    pretty_print(delete)
                                    
                            elif(cmd.startswith("del_target")):
                                target_id = input("[^] Target ID : ")
                                if(len(target_id) > 0):
                                    delete = gmp.delete_target(target_id)
                                    pretty_print(delete)

                            elif(cmd == "create_target"):
                                targetCreator(g)
                            
                            elif(cmd == "list_targets"):
                                g.ListTargets()

                            elif(cmd == "task_details"):
                                fl = input("[^] Filename to save as (XML) : ")
                                task_id = input("[^] Task ID : ")
                                if(len(task_id) > 0 and len(fl) > 0):
                                    details = gmp.get_task(task_id)
                                    rp = etree.ElementTree(details)
                                    rp.write(fl, pretty_print=True)
                                    
                            elif(cmd == "exit"):
                                exit(0)
                        
                            else :
                                print(bad, " Unknown command '{}', type help.".format(cmd))
                        except KeyboardInterrupt:
                            print("[X] Interrupt, Type exit to exit.")
                            pass

                        except Exception as e:
                            print(bad, "Error : " + str(e))
                            break

                except Exception as e:
                    print(bad, "Error : " + str(e))
                    # not error checking atm

            except Exception as e:
                print(bad, "Error : " + str(e))
    except Exception as e:
                print(bad, "Error : " + str(e))

if __name__ == "__main__":
    main()



