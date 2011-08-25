package com.youkaicountry.testrsvm;

import java.util.ArrayList;

public class ShooterThread
{
    public int codeloc = 0;
    public float[] registers;
    public float[] state = new float[30];
    public int sleep = 0;
    public ArrayList<Integer> children = new ArrayList<Integer>();
    public ArrayList<Integer> codestack = new ArrayList<Integer>();
    public ArrayList<Float> varstack = new ArrayList<Float>();
    public float[] threadvars = new float[8];
    
    public ShooterThread(int codeloc, int regsize)
    {
        if (codeloc < 0)
        {
            this.codeloc = 0;
        }
        else
        {
            this.codeloc = codeloc;
        }
        
        if (regsize < 0)
        {
            this.registers = new float[64];
        }
        else
        {
            this.registers = new float[regsize];
        }
        this.threadvars[0] = -1.0f;
        
    }
}
