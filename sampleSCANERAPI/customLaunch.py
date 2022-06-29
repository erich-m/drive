#!/usr/bin/python
import os
import time
import datetime
import traceback
import logging
import subprocess
import itertools
import sys

import scaner
import launchHtmlGui
import signal

def preexec_function():
    # Ignore the SIGINT signal by setting the handler to the standard
    # signal handler SIG_IGN.
    signal.signal(signal.SIGINT, signal.SIG_IGN)

class LauncherOption(scaner.ScanerApiOption):
    """Module options"""
    def __init__(self, default_config = 'NL_1.3',
                 default_frequency = 20, default_config_file="", steering_speed = 1.5, scenario=[], time_out = 30000):
        scaner.ScanerApiOption.__init__(self, 'SUPERVISOR', default_config, 
                                        default_frequency, default_config_file)

        self.add_option("-u", "--scenario", 
                    dest="scenario",
                    default=scenario,
                    action='append',
                    help="Scenario to launch [default: %default]")

        self.add_option("-v", "--verbose", 
                    dest="verbose",
                    action="store_true",
                    default=False,
                    help="Verbose mode [default: %default]")

        self.add_option("-t", "--time-out", 
                    dest="time_out",
                    type="int",
                    default=time_out,
                    help="Time out for SCANeR moduel to react to an order in ms [default: %default]")

        self.add_option("--no-daemon", 
                    dest="daemon",
                    action="store_false",
                    default=True,
                    help="Don't launch a daemon [default: %default]")

        self.add_option("--wait-before-start",
                    dest="wait_before_start",
                    type="int",
                    default=4.,
                    help="Time in second to wait before starting the SCANeR modules [default: %default]")

        self.add_option("--loop",
                    action="store_true",
                    default=False,
                    help="loop on the scenario (e.g; automatically start the next scenario at the end of the first one")

class ModulesNotOK(Exception):
    """Exception if a module died/is not reponsive"""
    def __init__(self):
        scaner.Simulation_UpdateProcessInfo()
        process_infos = (scaner.APIProcessInfo*scaner.Simulation_getProcessNumber())()
        scaner.Simulation_getAllProcessInfo(process_infos)
        bad_modules_lines = []
        for info in process_infos:
            id = scaner.Simulation_GetIdFromName(info.name)
            auto_launched = scaner.Simulation_IsProcessAutoLaunched(id)
            if auto_launched and self.test(info):
                bad_modules_lines.append("%s is in state %s"%(info.name, scaner.state_string(info.state)))
        self.value = "\n".join(bad_modules_lines)

    def test(self, info):
        return info.state == scaner.PS_DEAD

    def __str__(self):
        return self.value

class StateError(ModulesNotOK):
    """Execption if a state is not reach"""
    def __init__(self, state):
        self.state = state
        ModulesNotOK.__init__(self)
    
    def test(self, info):
        return info.state != self.state

    def __str__(self):
        return "SCANeR State %s not reached\n%s" %(scaner.state_string(self.state), self.value)

def wait_for_state(state, time_out):
    """ wait for a state to be reached
        time_out is in seconds, is negative this means no time out
        return false if the state can't be reached by all the module after time_out seconds
    """
    state_ok = False
    wait_time = 0.
    modules_to_track = []
    process_infos = (scaner.APIProcessInfo*scaner.Simulation_getProcessNumber())()
    scaner.Simulation_getAllProcessInfo(process_infos)
    for info in process_infos:
        if info.state != scaner.PS_DEAD\
            and info.name != "SUPERVISOR":
            modules_to_track.append(info.name)
    old_nb_modules_not_ok = -1

    while not state_ok:
        time.sleep(0.1)
        wait_time += 0.1
        scaner.Process_Run()
        scaner.Simulation_UpdateProcessInfo()
        process_infos = (scaner.APIProcessInfo*scaner.Simulation_getProcessNumber())()
        scaner.Simulation_getAllProcessInfo(process_infos)
        not_ok_module = []
        for info in process_infos:
            if info.state != state and info.name in modules_to_track:
                not_ok_module.append(info.name)
        state_ok = not not_ok_module
        if not_ok_module and len(not_ok_module) != old_nb_modules_not_ok:
            logging.info('Wait for modules to be in "%s":\n%s'%(scaner.state_string(state), "\n".join(not_ok_module)))
            old_nb_modules_not_ok = len(not_ok_module)
        if wait_time > time_out:
            break;
        not_ok_module = []

    return state_ok

class LauncherCommand:
    """Launcher command, can be 'start', load', 'pause', 'play', 'stop', 'unload', 'kill', 'exit'"""
    def __init__(self, command, arguments = []):
        self.command=command
        self.arguments = arguments
        pass

    def __str__(self):
        return "%(command)s, %(arguments)s"%self.__dict__

    @staticmethod
    def start():
        return LauncherCommand('start')
    @staticmethod
    def load(scenario):
        return LauncherCommand('load', [scenario])
    @staticmethod
    def pause():
        return LauncherCommand('pause')
    @staticmethod
    def play():
        return LauncherCommand('play')
    @staticmethod
    def stop():
        return LauncherCommand('stop')
    @staticmethod
    def unload():
        return LauncherCommand('unload')
    @staticmethod
    def kill():
        return LauncherCommand('kill')
    @staticmethod
    def exit():
        return LauncherCommand('exit')

class CommandError(Exception):
    """Exception raise when a command is not compatible with the launcher state"""
    def __init__(self, reason=""):
        self.reason = reason
    def __str__(self):
        return self.reason

class Launcher:
    """SCANeR Launcher"""
    def __init__(self):
        parser =LauncherOption('DEMO_PEKIN')
        (self.options, args) = parser.parse_args()
        print (self.options)
        log_dir = "./"
        try:
            if os.name=='nt':
                log_dir = os.environ["TEMP"] + '/'
            else:
                log_dir = '/tmp/'
        except:
            pass

        level=logging.INFO
        if self.options.verbose:
            level=logging.DEBUG

        date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        format='%(levelname)s: %(asctime)s %(message)s'
        logging.basicConfig(filename='%sLauncher%s.log'%(log_dir,date), format=format, level=level)

        # also redirect log to the console
        root = logging.getLogger()

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        formatter = logging.Formatter(format)
        ch.setFormatter(formatter)
        root.addHandler(ch)

        logging.info('Started')
        logging.info(str(self.options))

        if self.options.daemon:
            logging.info("Kill existing deamon")
            try:
                if os.name == 'nt':
                    out_contents = subprocess.check_output(["taskkill", "/T", "/F", "/IM", "SCANeRstudioDaemon.exe"], stderr=subprocess.STDOUT)
                else:
                    out_contents = subprocess.check_output(["killall", "SCANeRstudioDaemon"], stderr=subprocess.STDOUT)
                if out_contents:
                    logging.info(out_contents)
            except subprocess.CalledProcessError as e:
                logging.info("No daemon killed")
                logging.info(e.output)
            logging.info("Launch deamon")
            if os.name == 'nt':
                self.daemon = subprocess.Popen(['SCANeRstudioDaemon.exe', '-c', self.options.configuration])
            else:
                self.daemon = subprocess.Popen(['SCANeRstudioDaemon', '-c', self.options.configuration], preexec_fn=preexec_function)
            time.sleep(3)
        else:
            self.daemon = None

        self.break_loop = False
        scaner.Simulation_InitParams(self.options.configuration, self.options.frequency)

        self.commands = []
        self.commands.append(LauncherCommand.start())
        for scenario in self.options.scenario:
            self.commands.append(LauncherCommand.load(scenario))
            self.commands.append(LauncherCommand.pause())
            self.commands.append(LauncherCommand.play())

        self.read_stop_envent = True
        self.reset_state()
        self.scenario_played_number = 0
       
        #wait before iuntializing configuration and lauch modules
        if self.options.wait_before_start > 0:
            logging.info("Wait %ss before starting modules", self.options.wait_before_start)
            time.sleep(self.options.wait_before_start)
 
        #wait before iuntializing configuration and lauch modules
        scaner.Simulation_ChangeConfig(self.options.configuration)

        # register STOP to know when the scenario is ended
        scaner.Com_registerEvent("STOP")
        self.gui = launchHtmlGui.HTMLGui(self)
        self.gui.start()

    def state(self):
        """Return the simulation state as a string"""
        if self.paused:
            return "paused"
        if self.played:
            return "played"
        if self.loaded:
            return "loaded"
        if self.launched:
            return "launched"
        return "unknown"

    def reset_state(self):
        """Reset all state to False"""
        self.loaded = False
        self.launched = False
        self.paused = False
        self.played = False

    def add_command(self, command, reset = False):
        """add a command to the command buffer, reset the buffer if reset is True"""
        if reset:
            self.commands = []
        
        self.commands.append(command)
        
    def kill_all_except(self, modules):
        """kill all process except the given ones"""
        process_infos = (scaner.APIProcessInfo*scaner.Simulation_getProcessNumber())()
        scaner.Simulation_getAllProcessInfo(process_infos)
        modules_to_kill = []
        for info in process_infos:
            id = scaner.Simulation_GetIdFromName(info.name)
            auto_launched = scaner.Simulation_IsProcessAutoLaunched(id)
            if auto_launched and not info.name in modules:
                modules_to_kill.append(info.name)
        modules_to_kill_str = " ".join(modules_to_kill)
        logging.info("Kill %s", modules_to_kill_str)
        return scaner.Simulation_KillProcesses(modules_to_kill_str, self.options.time_out)
        
    def launch(self):
        """launch all process except the already launched ones"""
        process_infos = (scaner.APIProcessInfo*scaner.Simulation_getProcessNumber())()
        scaner.Simulation_getAllProcessInfo(process_infos)
        modules_to_launch = []
        for info in process_infos:
            id = scaner.Simulation_GetIdFromName(info.name)
            auto_launched = scaner.Simulation_IsProcessAutoLaunched(id)
            if auto_launched:
                if info.state == scaner.PS_DEAD:
                    modules_to_launch.append(info.name)
                elif info.state != scaner.PS_DAEMON:
                    scaner.Simulation_UnLoad();
        modules_to_launch_str = " ".join(modules_to_launch)
        logging.info("Launch %s", modules_to_launch_str)
        scaner.Simulation_StartProcess(modules_to_launch_str, self.options.time_out)
        return scaner.Simulation_WaitForState(modules_to_launch_str, scaner.PS_DAEMON, self.options.time_out)

    def get_log(self, line_nb=0):
        """return the last line_nb of the SCANeR log"""
        log_path = scaner.Utils_getPath('data/log')
        log = []
        for (dirpath, dirnames, filenames) in os.walk(log_path):
            for file in filenames:
                if 'SUPERVISOR.log' in file:
                    full_path = os.path.join(log_path, file)
                    current_log = []
                    for line in open(full_path):
                        if line[-1] == '\n':
                           line_log = line[:-1]
                        else:
                           line_log = line
                        log.append(line_log)

        return log[-line_nb:]

    def stop_scenario(self):
        unloaded = scaner.Simulation_Stop(1);
        unloaded = wait_for_state(scaner.PS_LOADED, self.options.time_out)
        if not unloaded:
            raise StateError(scaner.PS_LOADED)

    def execute_command(self, command):
        """accept and exectute, or not a command
            if return true the command was accepted, false rejected
            throw exception if the command can't be executed.
        """
        logging.debug("Execute command: %s"%command)
        if command.command == 'start':
            if self.loaded or self.paused or self.played:
                return False
            else:
                if not self.launched:
                    logging.info("Launch simulator")
                    if self.options.wait_before_start > 0:
                        logging.info("Wait %ss before starting modules", self.options.wait_before_start)
                        time.sleep(self.options.wait_before_start)
                    self.launched = self.launch()
                    if not self.launched:
                        raise StateError(scaner.PS_DAEMON)
                return True

        if command.command == 'load':
            if not self.launched:
                raise CommandError("Can not load a scenario when the simulator is not launched")
            elif self.paused or self.played:
                return False
            else:
                if not self.loaded:
                    current_scenario = command.arguments[0]
                    logging.info("Load scenario %s", current_scenario)
                    self.loaded = scaner.Simulation_LoadScenario(1, current_scenario)
                    self.loaded = wait_for_state(scaner.PS_LOADED, self.options.time_out)
                    if not self.loaded:
                        raise StateError(scaner.PS_LOADED)
                    time_launch =   time.clock()
                return True

        if command.command == 'pause':
            if not self.launched or not self.loaded:
                raise CommandError("Can not paused a scenario when the simulator is not launched or a scenario not loaded")
            else:
                if not self.paused:
                    logging.info("Pause scenario")
                    self.paused = scaner.Simulation_Pause(self.options.time_out)
                    self.paused = wait_for_state(scaner.PS_PAUSED, self.options.time_out)
                    if not self.paused:
                        raise StateError(scaner.PS_PAUSED)
                    self.played = False
                return True

        if command.command == 'play':
            if not self.launched:
                raise CommandError("Can not play a scenario when the simulator is not launched or a scenario not loaded")
            elif not self.loaded:
                for scenario in self.options.scenario:
                    self.commands.append(LauncherCommand.load(scenario))
                    self.commands.append(LauncherCommand.pause())
                    self.commands.append(LauncherCommand.play())
                    return True
            else:
                if not self.played:
                    logging.info("Start scenario")
                    self.played = scaner.Simulation_Play(self.options.time_out)
                    if not self.played:
                        raise StateError(scaner.PS_RUNNING)
                    old_steering = None
                    self.scenario_played_number =  self.scenario_played_number + 1
                    self.paused = False
                return True

        if command.command == 'stop':
            if not self.launched:
                raise CommandError("Can not stop a scenario if a scenario is not loaded")
            else:
                if self.loaded:
                    self.stop_scenario()
                    self.read_stop_envent = False
                return True

        if command.command == 'exit':
            logging.info("Stop simulator")
            raise KeyboardInterrupt
            return True

    def main_loop(self):
        """ Loop until ctrl-c"""
        while self.simulation_loop():
            pass
        if self.daemon:
            self.daemon.terminate()
        self.gui.stop_server = True
        logging.info('Stopped')

    def simulation_loop(self):
        """main SCANeR Api loop,
        return True if stop by ctrl-c, False if stop by an other reason"""
        ret = False
        counter = 0
        old_steering = None
        first_steering = False
        if self.options.loop:
            current_scenario_it = itertools.cycle(self.options.scenario);
        else:
            current_scenario_it = iter(self.options.scenario);
        try:
            time_launch = 0
            while not self.break_loop:

                # Process manager Run 
                scaner.Process_Run()
                scaner.Process_Wait()

                if self.commands:
                    command = self.commands[0]
                    if not self.execute_command(command):
                        logging.debug("Command ignored: %s"%command)
                    else:
                        self.commands.pop(0)
                else:
                     if self.options.loop:
                        for scenario in self.options.scenario:
                            self.commands.append(LauncherCommand.load(scenario))
                            self.commands.append(LauncherCommand.pause())
                            self.commands.append(LauncherCommand.play())

                                               

                for event in scaner.Events():
                    if event.state() == scaner.ST_Stop:
                        event.validate()
                        self.played = False
                        logging.info("End scenario")
                        logging.info("Unload scenario")
                        unloaded = scaner.Simulation_UnLoad(1);
                        unloaded = wait_for_state(scaner.PS_DAEMON, self.options.time_out)
                        if not unloaded:
                            raise StateError(scaner.PS_DAEMON)
                        self.loaded = False
                        if self.read_stop_envent:
                            ret = self.options.loop
                            if not self.options.loop:
                                self.break_loop = True
                        else:
                            self.read_stop_envent = True

                #Test simulation health
                if self.options.loop and not scaner.Simulation_AllProcessesOk():
                    raise ModulesNotOK()

                counter += 1
                #get a copy of the structure of exchange data 
                scaner.Com_updateInputs(scaner.UT_AllData)

        except KeyboardInterrupt:
            print ('Bye bye')
            ret = False
        except StopIteration:
            logging.info('no more scenario to launch')
            ret = self.options.loop
        except:
            logging.error(traceback.format_exc())
            ret = self.options.loop

        scaner.Simulation_KillAllProcesses(self.options.time_out)
        self.reset_state()
        logging.info("Iteration number %s, Scenario played number : %s", counter, self.scenario_played_number)
        return ret

def main():
    launcher = Launcher()
    launcher.main_loop()

if __name__ == '__main__':
    main()
