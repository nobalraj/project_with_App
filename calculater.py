from tkinter import *
import ast
import operator

class Calculater_1 :
    def __init__(self,app):
        app.title('Calculater')
        app.geometry('340x520')
        app.configure(background="#1e1e1e")
        app.resizable(False, False)

        self.expression=""

        self.entry=Entry(app,font=('Arial',24),bd=0,justify='right',bg="#2d2d2d",fg="white",insertbackground='white')
        self.entry.grid(row=0,column=0,columnspan=4,ipadx=3,ipady=10,pady=(20,10),padx=10,sticky="We")


        app.bind("<Key>", self.key_press)
        buttons=[
            ('7',1,0),('8',1,1),('9',1,2),('/',1,3),
            ('4',2,0),('5',2,1),('6',2,2),('*',2,3),
            ('1',3,0),('2',3,1),('3',3,2),('-',3,3),
            ('0',4,0),('.',4,1),('⌫',4,2),('+',4,3),
            ('(',5,0),(')',5,1),('C',5,2),('=',5,3),
        ]

        for btn in buttons:
            text=btn[0]
            row=btn[1]
            column=btn[2]
            columspace=btn[3] if len(btn) == 4 else 1

            Button(app,text=text,width=5,height=2,bd=0,font=('Arial',17),bg="#3c3c3c",fg="white",activebackground="#5a5a5a",activeforeground="yellow",command=lambda char=text:self.on_click(char)).grid(row=row,column=column,columnspan=columspace,sticky="nsew",padx=5,pady=5)

        for i in range(6):
            app.grid_rowconfigure(i,weight=1)
        for j in range(4):
            app.grid_columnconfigure(j,weight=1)

    def on_click(self,char):
        if char =='C':
            self.expression=""
            self.entry.delete(0,END)
        elif char=='⌫':
            self.expression=self.expression[:-1]
            self.entry.delete(0,END)
            self.entry.insert(END,self.expression)
        elif char=='=':
            try:

                result=self.safe_eval(self.expression)
                self.entry.delete(0,END)
                self.entry.insert(END,str(result))
                self.expression=str(result)
            except Exception :
                self.entry.delete(0,END)
                self.entry.insert(END,'Error')
                self.expression=""

        else:
            self.expression += str(char)
            self.entry.delete(0,END)
            self.entry.insert(END,self.expression)
    def key_press(self,event):
        key=event.char
        if key in '0123456789+-*/().':
            self.on_click(key)
        elif key == '\r':  # Enter key
            self.on_click('=')
        elif key == '\x08':  # Backspace
            self.on_click('⌫')
        elif key.lower() == 'c':
            self.on_click('C')


    def safe_eval(self, expr):
        node=ast.parse(expr,mode='eval')
        operators={
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg

        }

        def _evel(node):
            if isinstance(node,ast.Expression):
                return _evel(node.body)
            elif isinstance(node,ast.BinOp):
                left=_evel(node.left)
                right=_evel(node.right)
                op=operators[type(node.op)]
                return op(left,right)
            elif isinstance(node,ast.UnaryOp):
                operand=_evel(node.operand)
                op=operators[type(node.op)]
                return op(operand)
            elif isinstance(node,ast.Constant):
                if isinstance(node.value,(int,float)):
                    return node.value
                else:
                    raise TypeError("Onlu numeric value allowed")
            else:
                raise TypeError("Unsupported  Expression")
        return _evel(node)



if __name__ =='__main__':
    root=Tk()
    calculater=Calculater_1(root)
    root.mainloop()
