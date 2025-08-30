import os, sys, traceback
from pathlib import Path; sys.path.append( str(Path(__file__).parent.parent) )

from U2.base import U2_Device
from U2.enums import TaskType, Wtype
from U2.task import Task
from U2.debug import debugLog
from U2.process import start_adb_shell_pipes


class _Bot( U2_Device ):


    def __init__( self, **kwargs ):
        self.tasks = {
            # TaskType.value : Task()
        }
        self.current_task : Task = None
        self.current_task_number = 0

        self.prev_task_number = 0
        self.next_task_number = 0
    
        self.parent_match_timeout = 400
        self.check_selector = {}

        super().__init__( **kwargs )


    def add_task( self, task : Task, name : str = None ):
        # Append task to map for quick access
        # Tasktype enum will get updated every call
        # TaskType.t<task.number> = task.number
        assert isinstance( task, Task )

        number = task.number
        setattr( TaskType, f"t{number}" if not name else name, task.number )

        # Add task to map and access via number or enum TaskType.t<number>
        self.tasks[ number ] = task


    def get_prev_task( self ) -> Task:
        return self.tasks[ self.prev_task_number ]


    def get_next_task( self ) -> Task:
        return self.tasks[ self.next_task_number ]


    def default_match( self ) -> dict:
        # Default match function if current task match function is not defined and set
        current_task = self.current_task
        ui = self.waitElement( current_task.match_selector, timeout = current_task.match_selector_timeout )

        if ui == 'FAILED':
            log = f"[{self}] selector match failed @task.number[{current_task.number}]"
            debugLog( log )

            return None

        if not ui and current_task.match_alt:
            ui = self.waitElement( current_task.match_alt, timeout = 0.2 )
            log = f"[{self}] selector not found using match alt instead <status:{'Ok' if type(ui) not in (type(None),str) else 'Failed'}> @task.number[{current_task.number}]"
            debugLog( log )

            if type(ui) in [ type(None), str ]:
                return None

        ui_info = self.getInfo( ui )

        if current_task.match_class_inclusion_list:
            if not ui_info['className'] in current_task.match_class_inclusion_list:

                log = f"[{self}] class_name not found in list : [{ui_info['text']}|{ui_info['className']}] @task.number[{current_task.number}]"
                debugLog( log )

                for class_name in current_task.match_class_inclusion_list:
                    ui = self.waitElement( current_task.match_selector | { 'className' : class_name }, timeout=0.2 )

                    if type(ui) not in [ type(None), str ]:
                        break

                if not ui or ui == 'FAILED':        
                    log = f"[{self}] element not found using inclusion list : [{ui}] @task.number[{current_task.number}]"
                    debugLog( log )

                    return None
                ui_info = self.getInfo( ui )
        return ui_info


    def get_current_match( self ) -> dict:
        # Search for parent match
        func = self.current_task.match_function
        return func() if func else self.default_match()


    def next_task_function( self, ui_info : dict = None ):
        self.check_selector = self.current_task.check_selector or {'text' : ui_info['text'], 'className' : ui_info['className']}

        self.prev_task_number = self.current_task.prev_task_number
        self.next_task_number = self.current_task.next_task_number

        self.current_task_number = TaskType.check


    def set_next_task( self, ui_info:dict = None ):
        # Run task next_task function setup
        n_func = self.current_task.next_function
        n_func( ui_info ) if n_func else self.next_task_function( ui_info )


    def handle_callback( self ):
        ui_info = None

        if self.current_task.match_selector:
            ui_info = self.get_current_match()
            
            if not ui_info:
                #debugLog( f"Ui info None: handle_callback @task[{self.current_task.number}]" )
                return

        # Task action
        result = self.current_task.callback( ui_info )
        if not result:
            debugLog( f"Action failed @task[{self.current_task.number}]" )
            return
        # Next task
        self.set_next_task( ui_info )


    def mainloop( self ):
        while self.running and not _Bot.sig_term:
            try:
                self.current_task = self.tasks[ self.current_task_number ]
                self.handle_callback() if self.current_task.bHandle_callback else self.current_task.callback()

            except Exception as e:
                traceback.print_exception( type(e), e, e.__traceback__, file=sys.stdout )
                break

            except KeyboardInterrupt:
                _Bot.sig_term = True
                break


    def run( self ):
        if not self.tasks:
            print(f"{self} task list is empty")
            return

        if not self.device:
            print(f"{self} device session is not initialized")
            return

        start_adb_shell_pipes()
        self.mainloop()


if __name__=='__main__':
    pass
