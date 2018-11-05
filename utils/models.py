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
            if not arg.startswith("_")
        }

        transitions = [
            self.find_additional_args_for_transitions(trans_kwargs)
            for trans_kwargs in machine_args["transitions"]
        ]
        machine_args.update({"transitions": transitions})

        machine_args.update({"model": self, "initial": self.state})
        self.machine = Machine(**machine_args)

    def find_additional_args_for_transitions(self, existing):
        args = existing.copy()
        trigger = args.get("trigger")

        # Add prepare function if available
        # TODO: should this be conditions instead? or add it as well
        # use getattr, and check that prepare and condition are functions
        prepare_func = f"prepare_{trigger}"
        if hasattr(self, prepare_func):
            args.update(dict(prepare=prepare_func))

        return args
