class Static:
    def getStyle(self,input_box):
        style='<style>\n'+\
            '#%s {\n' % input_box +\
                'font-size: 15px;\n'+\
                'border-bottom: 1px solid #ddd;\n'+\
            '}\n'+\
            '.dropdown-content {\n'+\
                'visibility: hidden;\n' +\
                'position: absolute;\n'+\
                'background-color:#f6f6f6;\n'+\
                'max-height: 308px;\n'+\
                'overflow: auto;\n'+\
                'border: 1px solid #ddd;\n'+\
                'z-index: 1;\n'+\
            '}\n'+\
            '.dropdown-content a {\n'+\
                'color: black;\n'+\
                'padding: 12px 16px;\n'+\
                'text-decoration: none;\n'+\
                'display: block;\n'+\
                'cursor: pointer;\n' +\
            '}\n'+\
            '.dropdown-content a:hover {\n' +\
                'background-color: #ddd;\n'+\
            '}\n'+\
        '</style>\n'
        return style
    def getScript(self,input_box,default_value):
        script= '<script>\n'+\
                    'var input_%s, a_%s, i, select_%s = -1, visible_a_%s;\n'% (input_box,input_box,input_box,input_box)+\
                    'input_%s = document.getElementById("%s");\n' %(input_box,input_box) +\
                    'input_%s_hidden=document.getElementById("%s_hidden");\n' % (input_box, input_box) +\
                    'div_%s = document.getElementById("%s_Dropdown");\n' % (input_box, input_box) +\
                    'visible_a_%s = a_%s = div_%s.getElementsByTagName("a");\n' % (input_box,input_box,input_box) +\
                    'div_%s.style.width=input_%s.clientWidth+"px";\n' % (input_box, input_box) +\
                    '%s' % default_value +\
                    'input_%s.addEventListener("click", function(event){\n'%input_box +\
                        'if(div_%s.style.visibility==="visible"){\n' % input_box +\
                            'div_%s.style.visibility="hidden";\n' % input_box +\
                        '}\n' +\
                        'else{\n' +\
                            'div_%s.style.visibility="visible";\n' % input_box +\
                        '}\n' +\
                    '});\n'+\
                    'input_%s.addEventListener("keyup", function(event){\n' % input_box +\
                        'event.preventDefault();\n'+\
                        'if(event.keyCode === 13){\n' +\
                            'if(div_%s.style.visibility==="visible"){\n' % input_box +\
                                'div_%s.style.visibility="hidden";\n' % input_box +\
                            '}\n' +\
                            'else{\n' +\
                                'div_%s.style.visibility="visible";\n' % input_box +\
                            '}\n' +\
                        '}\n' +\
                        'else{\n' +\
                            'input_%s_hidden.value=""\n' % input_box +\
                            'div_%s.style.visibility="visible";\n' % input_box +\
                        '}\n' +\
                        'if(select_%s >= 0){\n' % input_box +\
                            'visible_a_%s[select_%s].style.backgroundColor="#f6f6f6";\n' % (input_box,input_box) +\
                        '}\n'+\
                        'if(event.keyCode === 38 || event.keyCode === 40){\n' +\
                            'if(event.keyCode === 38){\n'+\
                                'if(select_%s > 0){\n' % input_box +\
                                    'select_%s -= 1;\n' % input_box+\
                                '}\n'+\
                                'else{\n'+\
                                    'select_%s=visible_a_%s.length-1;\n' % (input_box, input_box) +\
                                '}\n'+\
                            '}\n'+\
                            'else{\n'+\
                                'if(select_%s < visible_a_%s.length - 1){\n' % (input_box, input_box) +\
                                    'select_%s += 1;\n' % input_box +\
                                '}\n' +\
                                'else{\n' +\
                                    'select_%s=0;\n' % input_box +\
                                '}\n' +\
                            '}\n'+\
                            'input_%s_hidden.value=visible_a_%s[select_%s].getAttribute("value")\n' % (input_box,input_box,input_box) +\
                            'input_%s.value=visible_a_%s[select_%s].innerHTML;\n' % (input_box, input_box, input_box) +\
                            'visible_a_%s[select_%s].style.backgroundColor="#ddd";\n' % (input_box, input_box) +\
                        '}\n'+\
                        'else{\n'+\
                            'select_%s=-1;\n' % input_box +\
                            'visible_a_%s=[];\n' % input_box +\
                            'filter=input_%s.value.toUpperCase();\n' % input_box +\
                            'for(i=0;i< a_%s.length;i++){\n' % input_box +\
                                'if(a_%s[i].innerHTML.toUpperCase().search(filter) > -1){\n' % input_box +\
                                    'a_%s[i].style.display="";\n' % input_box +\
                                    'visible_a_%s.push(a_%s[i]);\n' % (input_box, input_box) +\
                                '}\n'+\
                                'else{\n'+\
                                    'a_%s[i].style.display="none";\n' % input_box +\
                                '}\n'+\
                            '}\n'+\
                            'if(visible_a_%s.length==1 && event.keyCode !==8){\n' % input_box +\
                                'input_%s_hidden.value=visible_a_%s[0].getAttribute("value")\n' % (input_box, input_box) +\
                                'input_%s.value=visible_a_%s[0].innerHTML;\n' % (input_box, input_box) +\
                            '}\n' +\
                        '}\n'+\
                    '});\n'+\
                    'div_%s.addEventListener("click", function(e){\n' % input_box +\
                        'input_%s_hidden.value=e.target.getAttribute("value");\n' % input_box +\
                        'input_%s.value=e.target.innerHTML;\n' % input_box +\
                        'if(div_%s.style.visibility==="visible"){\n' % input_box +\
                            'div_%s.style.visibility="hidden";\n' % input_box +\
                        '}\n' +\
                        'else{\n' +\
                            'div_%s.style.visibility="visible";\n' % input_box +\
                        '}\n' +\
                    '});\n'+\
                    'document.addEventListener("click",function(e){\n'+\
                        'if(e.target.getAttribute("id") != "%s"){\n' %input_box +\
                            'div_%s.style.visibility="hidden";\n' % input_box +\
                        '}\n'+\
                    '});\n'+\
                    '$("form").bind("keypress", function(e){\n'+\
                        'if(e.keyCode === 13){\n'+\
                            'e.preventDefault();\n'+\
                            'return false;\n'+\
                        '}\n'+\
                    '});\n'+\
                '</script>\n'
        return script
