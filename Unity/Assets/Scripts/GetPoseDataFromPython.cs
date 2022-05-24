using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using System.Threading;
using System.IO;
using System.Text;

public class GetPoseDataFromPython 
{
    private static Process pythonProc = new Process();
    public delegate void PosReceiveHandler(int posX, int posY);
    public delegate void HeadReceiveHandler(int headScale);
    public delegate void TurnReceiveHandler(int pitch, int yaw, int roll);

    public event PosReceiveHandler posSendEvent;
    public event HeadReceiveHandler headSendEvent;
    public event TurnReceiveHandler turnSendEvent;

    // Start is called before the first frame update
    public GetPoseDataFromPython()
    {
        pythonProc.StartInfo.FileName = "C:/Users/aass7/AppData/Local/Programs/Python/Python38/python.exe";
        pythonProc.StartInfo.Arguments = "-u C:/HealthyEmoji/Python/main.py";
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

        if(!poseData[0].Equals("FromPython") || poseData.Length > 7)
        {
            return;
        }

        /*
        foreach(string str in poseData)
        {
            UnityEngine.Debug.Log(str);
        }*/

        posSendEvent(int.Parse(poseData[1]), int.Parse(poseData[2]));
        headSendEvent(int.Parse(poseData[3]));
        turnSendEvent(int.Parse(poseData[4]), int.Parse(poseData[5]), int.Parse(poseData[6]));
    }
}

