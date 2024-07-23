from colorama import init,Fore,Back,Style,just_fix_windows_console
from typing import Callable
init(autoreset=True)
just_fix_windows_console()
r=Style.RESET_ALL
class Logger():
    def __init__(self,level:int=1,icons:tuple[str,str,str,str,str,str]=('$','~','!','-','x','?'),brackets:tuple[str,str]=('[',']'),
                 styles:tuple[str,str,str,str,str,str,str]=(Fore.WHITE+Style.DIM,Fore.CYAN+Style.BRIGHT,
                                                            Fore.WHITE+Style.BRIGHT,Fore.YELLOW+Style.BRIGHT,
                                                            Fore.RED+Style.BRIGHT,Fore.WHITE+Style.BRIGHT+Back.RED,
                                                            Fore.MAGENTA+Style.BRIGHT),handler:Callable[[str,int],bool]=lambda x,y:True) -> None:
        if not level in (0,1,2,3,4): raise ValueError(f"Level should be an integer between 0 and 4, but level={level} was given. (Questions cannot be disabled)")
        if not len(brackets)==2: raise ValueError(f"Brackets must be a list of 2 elements: left bracket and right bracket, but {len(brackets)} elements were given.")
        if not len(icons)==6: raise ValueError(f"Icons must be a list of 6 elements, but {len(icons)} elements were given.")
        if not len(styles)==7: raise ValueError(f"Styles must be a list of 7 elements, but {len(icons)} elements were given.")
        self.level:int=level
        self.icons:tuple=icons
        self.brackets:tuple=brackets
        self.styles:tuple=styles
        self.strformat:str="{}"+self.brackets[0]+r+"{}{}"+r+"{}"+self.brackets[1]+" "+r+"{}{}"
        self.handler:Callable[[str,int],bool]=handler
    def format(self,msg:str,level:int=1)->str:
        if not level in (0,1,2,3,4,5): raise ValueError(f"Level should be an integer between 0 and 5, but level={level} was given.")
        return self.strformat.format(self.styles[0],self.styles[level+1],self.icons[level],self.styles[0],self.styles[level+1],msg)
    def refresh(self)->None:
        if not self.level in (0,1,2,3,4,5): raise ValueError(f"Level should be an integer between 0 and 5, but level={level} was given.")
        if not len(self.brackets)==2: raise ValueError(f"Brackets must be a list of 2 elements: left bracket and right bracket, but {len(brackets)} elements were given.")
        if not len(self.icons)==6: raise ValueError(f"Icons must be a list of 6 elements, but {len(icons)} elements were given.")
        if not len(self.styles)==7: raise ValueError(f"Styles must be a list of 7 elements, but {len(icons)} elements were given.")
        self.strformat:str="{}"+self.brackets[0]+r+"{}{}"+r+"{}"+self.brackets[1]+" "+r+"{}{}"
    def handle_log(self,msg:str,level:int=1)->str:
        if level<self.level: return ""
        if not self.handler(msg,level): return ""
        if level==5:
            return input(self.format(msg,level))
        else:
            print(self.format(msg,level))
            return ""
    def debug(self,msg:str)->None:
        self.handle_log(msg,0)
    def info(self,msg:str)->None:
        self.handle_log(msg,1)
    def warn(self,msg:str)->None:
        self.handle_log(msg,2)
    def error(self,msg:str)->None:
        self.handle_log(msg,3)
    def crit(self,msg:str)->None:
        self.handle_log(msg,4)
    def ask(self,msg:str)->str:
        return self.handle_log(msg+" > ",5)
    