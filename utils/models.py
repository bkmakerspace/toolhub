from transitions import Machine


class StateMachineMixin:
    class StateMachine:
        states = []
        transitions = []
        auto_transitions = False
        send_event = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        machine_args = {
            arg: getattr(self.StateMachine, arg)
            for arg in dir(self.StateMachine)
            if not arg.startswith('_')
        }
        machine_args.update({
            'model': self,
            'initial': self.state,
        })
        self.machine = Machine(**machine_args)
