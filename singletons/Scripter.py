import Stringtools
import singletons.World as World
import classes.Message as Message


def ClickOn(UIElementName):
    return f"""
    select_ui_element {UIElementName}
    simulate_mouse_click lclick_down
    simulate_mouse_click lclick_up
    """


# You can use | for new line inside message text body (titles have always one line)
def MessageInfo(Title, Text, Image="script_prompt"):
    hash = Stringtools.Hash(Title + Text)
    message = Message.Message(Title, Text)
    if message.Id not in [m.Id for m in World.World.Messages]:
        World.World.Messages.append(message)
    return f"""
    message_prompt
        {{
        flag_counter dummy_f
        result_counter dummy_r
        title {hash}_TITLE
        body {hash}_BODY
        image {Image}
        }}
    """


def Multiply(x, y):
    return int(x) * int(y)


def MultiplyNegative(x, y):
    return int(x) * int(y) * -1


def Repeat(n):
    temp = "x" * n
    result = list(temp)
    return result


def Range(rangeFrom, rangeTo):
    result = range(rangeFrom, rangeTo+1)
    result = [str(i) for i in result]
    return result
