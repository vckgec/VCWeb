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
    def getScript(self,input_box,dropdown_div):
        script= '<script>\n'+\
                    'var input, filter, ul, li, a, i, select = -1, visible_a;\n'+\
                    'input = document.getElementById("%s");\n' %input_box +\
                    'input_hidden=document.getElementById("%s_hidden");\n' % input_box +\
                    'div = document.getElementById("%s");\n' %dropdown_div +\
                    'visible_a = a = div.getElementsByTagName("a");\n'+\
                    'div.style.width=input.clientWidth+"px";\n'+\
                    'input.addEventListener("click", function(event){\n'+\
                        'if(div.style.visibility==="visible"){\n'+\
                            'div.style.visibility="hidden";\n'+\
                        '}\n'+\
                        'else{\n'+\
                            'div.style.visibility="visible";\n'+\
                        '}\n'+\
                    '});\n'+\
                    'input.addEventListener("keyup", function(event){\n'+\
                        'event.preventDefault();\n'+\
                        'if(event.keyCode === 13){\n'+\
                            'if(div.style.visibility==="visible"){\n'+\
                                'div.style.visibility="hidden";\n'+\
                            '}\n'+\
                            'else{\n'+\
                                'div.style.visibility="visible";\n'+\
                            '}\n'+\
                        '}\n'+\
                        'else{\n'+\
                            'input_hidden.value=""\n'+\
                            'div.style.visibility="visible";\n'+\
                        '}\n'+\
                        'if(select >= 0){\n'+\
                            'visible_a[select].style.backgroundColor="#f6f6f6";\n'+\
                        '}\n'+\
                        'if(event.keyCode === 38 || event.keyCode === 40){\n'+\
                            'if(event.keyCode === 38){\n'+\
                                'if(select > 0){\n'+\
                                    'select -= 1;\n'+\
                                '}\n'+\
                                'else{\n'+\
                                    'select=visible_a.length-1;\n'+\
                                '}\n'+\
                            '}\n'+\
                            'else{\n'+\
                                'if(select < visible_a.length - 1){\n'+\
                                    'select += 1;\n'+\
                                '}\n'+\
                                'else{\n'+\
                                    'select=0;\n'+\
                                '}\n'+\
                            '}\n'+\
                            'input_hidden.value=visible_a[select].getAttribute("value")\n'+\
                            'input.value=visible_a[select].innerHTML;\n'+\
                            'visible_a[select].style.backgroundColor="#ddd";\n'+\
                        '}\n'+\
                        'else{\n'+\
                            'select=-1;\n'+\
                            'visible_a=[];\n'+\
                            'filter=input.value.toUpperCase();\n'+\
                            'for(i=0;i< a.length;i++){\n'+\
                                'if(a[i].innerHTML.toUpperCase().search(filter) > -1){\n'+\
                                    'a[i].style.display="";\n'+\
                                    'visible_a.push(a[i]);\n'+\
                                '}\n'+\
                                'else{\n'+\
                                    'a[i].style.display="none";\n'+\
                                '}\n'+\
                            '}\n'+\
                            'if(visible_a.length==1 && event.keyCode !==8){\n'+\
                                'input_hidden.value=visible_a[0].getAttribute("value")\n'+\
                                'input.value=visible_a[0].innerHTML;\n'+\
                            '}\n'+\
                        '}\n'+\
                    '});\n'+\
                    'div.addEventListener("click", function(e){\n'+\
                        'input_hidden.value=e.target.getAttribute("value");\n'+\
                        'input.value=e.target.innerHTML;\n'+\
                        'if(div.style.visibility==="visible"){\n'+\
                            'div.style.visibility="hidden";\n'+\
                        '}\n'+\
                        'else{\n'+\
                            'div.style.visibility="visible";\n'+\
                        '}\n'+\
                    '});\n'+\
                    'document.addEventListener("click",function(e){\n'+\
                        'if(e.target.getAttribute("id") != "%s"){\n' %input_box +\
                            'div.style.visibility="hidden";\n'+\
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

