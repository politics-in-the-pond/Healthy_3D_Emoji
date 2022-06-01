using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FaceOSCrecievePose : MonoBehaviour
{
    private float posX;
    private float posY;
    private float sizeHead;
    private float pitch;
    private float yaw;
    private float roll;

    private float ri=1f;
    private float le=1f;

    private float th1=45.0f;
    private float th2=1000.0f;
    private int is_poseWrong = 0;

    public GameObject face;
    public GameObject eye_right;
    public GameObject eye_left;
    public GameObject backlight;

    // Start is called before the first frame update
    void Start()
    {
        sizeHead = 1;
        GetPoseDataFromPython pose = new GetPoseDataFromPython();
        pose.posSendEvent += new GetPoseDataFromPython.PosReceiveHandler(pos);
        pose.headSendEvent += new GetPoseDataFromPython.HeadReceiveHandler(scaleHead);
        pose.turnSendEvent += new GetPoseDataFromPython.TurnReceiveHandler(turn);
        pose.earSendEvent += new GetPoseDataFromPython.EarReceiveHandler(ear);
        pose.poseSendEvent += new GetPoseDataFromPython.PoseReceiveHandler(poseDetection);
    }

    // Update is called once per frame
    void Update()
    {
        face.transform.position = new Vector3(-posX, posY, 0.0f); 
        face.transform.localScale = new Vector3(sizeHead, sizeHead, sizeHead);

        Quaternion target = Quaternion.Euler(pitch, -yaw, roll);

        face.transform.rotation = Quaternion.Slerp(face.transform.rotation, target, Time.deltaTime * 5.0f);

        eye_right.transform.localScale = new Vector3(1f, 1f, ri);
        eye_left.transform.localScale = new Vector3(1f, 1f, le);

        if(is_poseWrong==0){
            backlight.GetComponent<Light>().color = Color.white;
        }else{
            backlight.GetComponent<Light>().color = Color.red;
        }
    }

    public void pos(int x, int y)
    {
        posX = map(x, 140, 670, -2, 2);
        posY = map(y, 0, 480, 0.5f, -0.5f);
    }

    public void scaleHead(int head)
    {
       sizeHead = map(head,70,370,0.5f,2);
    }

    public void turn(int r, int y, int p)
    {
        roll = map(r, -80f, 80f, 30, -30);

        yaw = map(y, -55, 55f, -30, 30);

        pitch = map(p, -50f, 0f, 10, -10);
    }

    public static float map(float x, float x1, float x2, float y1, float y2)
    {
        var m = (y2 - y1) / (x2 - x1);
        var c = y1 - m * x1; // point of interest: c is also equal to y2 - m * x2, though float math might lead to slightly different results.

        return m * x + c;
    }

    public void ear(float right, float left){
        ri = 1/(right-2.5f);
        if(ri>1)
            ri=1;
        if(ri<0.01f)
            ri=0.01f;
        le = 1/(left-2.5f);
        if(le>1)
            le=1;
        if(le<0.01f)
            le=0.01f;
    }

    public void poseDetection(double threshold1, double threshold2){
        if(threshold1>th1 && threshold2<th2){
            is_poseWrong = 1;
        }else{
            is_poseWrong = 0;
        }
    }
}
