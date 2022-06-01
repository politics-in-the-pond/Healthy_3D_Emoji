using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using System.Threading;
using System.IO;
using System.Text;
using System;

public class GetPoseDataFromPython 
{
    private static Process pythonProc = new Process();
    public delegate void PosReceiveHandler(int posX, int posY);
    public delegate void HeadReceiveHandler(int headScale);
    public delegate void TurnReceiveHandler(int pitch, int yaw, int roll);
    public delegate void EarReceiveHandler(float right, float left);
    public delegate void PoseReceiveHandler(double threshold1, double threshold2);

    public event PosReceiveHandler posSendEvent;
    public event HeadReceiveHandler headSendEvent;
    public event TurnReceiveHandler turnSendEvent;
    public event EarReceiveHandler earSendEvent;
    public event PoseReceiveHandler poseSendEvent;


    // Start is called before the first frame update
    public GetPoseDataFromPython()
    {
        pythonProc.StartInfo.FileName = "python";
        pythonProc.StartInfo.Arguments = "-u ../Python/main.py";
        pythonProc.StartInfo.UseShellExecute = false;
        pythonProc.StartInfo.CreateNoWindow = true;
        pythonProc.StartInfo.RedirectStandardOutput = true;
        pythonProc.StartInfo.RedirectStandardInput = true;
        pythonProc.StartInfo.RedirectStandardError = true;
        pythonProc.EnableRaisingEvents = true;

        pythonProc.ErrorDataReceived += process_OutputDataReceived;
        pythonProc.OutputDataReceived += process_OutputDataReceived;

        pythonProc.Start();
        pythonProc.BeginErrorReadLine();
        pythonProc.BeginOutputReadLine();
    }


    private void process_OutputDataReceived(object sender, DataReceivedEventArgs e)
    {
        if(e.Data == null || e.Data.GetType() != typeof(string))
        {
            return;
        }

        string[] poseData = e.Data.Split(" ");

        if(poseData[0].Equals("FromPython") && poseData.Length == 11)
        {
            posSendEvent(int.Parse(poseData[1]), int.Parse(poseData[2]));
            headSendEvent(int.Parse(poseData[3]));
            turnSendEvent(int.Parse(poseData[4]), int.Parse(poseData[5]), int.Parse(poseData[6]));
            try{
                earSendEvent(float.Parse(poseData[9]), float.Parse(poseData[10]));
                poseSendEvent(double.Parse(poseData[7]), double.Parse(poseData[8]));
            }
            catch(Exception ex){
                UnityEngine.Debug.Log(ex);
            }

        
        }//else if(poseData[0].Equals("FromPythonPose") && poseData.Length == 3){
           // poseSendEvent(float.Parse(poseData[1]), float.Parse(poseData[2]));

        //}else if(poseData[0].Equals("FromPythonEar") && poseData.Length == 3){
          //  earSendEvent(float.Parse(poseData[1]), float.Parse(poseData[2]));

        else{
            UnityEngine.Debug.Log(e.Data);
        }

        /*
        foreach(string str in poseData)
        {
            UnityEngine.Debug.Log(str);
        }*/

        }
}

