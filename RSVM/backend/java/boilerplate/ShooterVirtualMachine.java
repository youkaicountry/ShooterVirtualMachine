package com.youkaicountry.testrsvm;

import java.util.ArrayList;
import java.util.Iterator;

interface ShooterVirtualMachine
{
    Iterator getThreadIDs();
    float getState(int threatid, String state);
    ArrayList<Integer> getThreadChildren(int threadid); 
    int getThreadParent(int threadid);
    void setPlayerPosition(float x, float y);
    int spawnThread(int initloc, float x, float y, float angle, int parent);
    void run();
}
