import java.util.ArrayList;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.Stack;
import java.util.TreeMap;

@SuppressWarnings("all")
class RSVM implements ShooterVirtualMachine
   {
    public Hashtable<Integer, ShooterThread> threads;
    public Hashtable<String, Integer> statename;
    public float[] mem;
    public Random r = null;
    public float[] vmdata = new float[2];
    public int regsize;
    public int stacksize;
    public int nextthread;
    private float tf1, tf2, tf3;
    private int ti1, ti2;
    private Stack<ShooterThread> ready_threads;
    
    //try 64, 32, 32, 32, null
    //if r is null, a new one is made.
    public RSVM(int memsize, int regsize, int stacksize, int initthreads, Random r)
    {
        if (r == null) {this.r = new Random();}
        this.ready_threads = new Stack<ShooterThread>();
        for (int i = 0; i < initthreads; i++)
        {
            this.ready_threads.push(new ShooterThread(0, regsize, stacksize));
        }
        this.threads = new Hashtable<Integer, ShooterThread>();
        this.mem = new float[memsize];
        this.regsize = regsize;
        this.stacksize = stacksize;
        this.nextthread = 0;
        this.mem[0] = 0;
        this.mem[1] = 0;
        this.statename = new Hashtable<String, Integer>();
        statename.put("x", new Integer(0));
        statename.put("__x", new Integer(0));
        statename.put("y", new Integer(1));
        statename.put("__y", new Integer(1));
        statename.put("angle", new Integer(2));
        statename.put("__angle", new Integer(2));
        statename.put("targetx", new Integer(3));
        statename.put("__targetx", new Integer(3));
        statename.put("targety", new Integer(4));
        statename.put("__targety", new Integer(4));
        statename.put("returnval", new Integer(5));
        statename.put("__returnval", new Integer(5));
        statename.put("condition", new Integer(6));
        statename.put("__condition", new Integer(6));
        statename.put("sprite", new Integer(27));
        statename.put("__sprite", new Integer(27));
        statename.put("radius", new Integer(28));
        statename.put("__radius", new Integer(28));
        return;
    }
    
    private int block2FuncCall(ShooterThread th)
    {
        int retval = 0;
        switch (th.codeloc)
        {
           case 0: retval = this.f0(th); break;
           case 1: retval = this.f1(th); break;
           case 2: retval = this.f2(th); break;
           case 3: retval = this.f3(th); break;
           case 4: retval = this.f4(th); break;
           case 5: retval = this.f5(th); break;
           case 6: retval = this.f6(th); break;
           case 7: retval = this.f7(th); break;
           case 8: retval = this.f8(th); break;
           case 9: retval = this.f9(th); break;
           case 10: retval = this.f10(th); break;
           case 11: retval = this.f11(th); break;
           case 12: retval = this.f12(th); break;
           case 13: retval = this.f13(th); break;
           case 14: retval = this.f14(th); break;
           case 15: retval = this.f15(th); break;
           case 16: retval = this.f16(th); break;
           case 17: retval = this.f17(th); break;
           case 18: retval = this.f18(th); break;
           case 19: retval = this.f19(th); break;
           case 20: retval = this.f20(th); break;
           case 21: retval = this.f21(th); break;
           case 22: retval = this.f22(th); break;
           case 23: retval = this.f23(th); break;
           case 24: retval = this.f24(th); break;
           case 25: retval = this.f25(th); break;
           case 26: retval = this.f26(th); break;
           case 27: retval = this.f27(th); break;
           case 28: retval = this.f28(th); break;
           case 29: retval = this.f29(th); break;
           case 30: retval = this.f30(th); break;
           case 31: retval = this.f31(th); break;
           case 32: retval = this.f32(th); break;
           case 33: retval = this.f33(th); break;
           case 34: retval = this.f34(th); break;
           case 35: retval = this.f35(th); break;
           case 36: retval = this.f36(th); break;
           case 37: retval = this.f37(th); break;
           case 38: retval = this.f38(th); break;
        }
        return retval;
    }
    
    public int spawnThread(int initloc, float x, float y, float angle, int parent)
    {
        int nt = this.nextthread;
        ShooterThread st;
        if (this.ready_threads.empty())
        {
            st = new ShooterThread(initloc, this.regsize, this.stacksize);
        }
        else
        {
            st = (ShooterThread)(this.ready_threads.pop());
            st.clear(initloc);
        }
        this.threads.put(nt, st);
        st.state[0] = x;
        st.state[1] = y;
        st.state[2] = angle;
        st.threadvars[1] = nt;
        if (parent >= 0)
        {
            st.threadvars[0] = parent;
            this.threads.get(parent).children.add(this.threads.get(parent).children.size(), nt);
        }
        else
        {
            st.threadvars[0] = -1;
        }
        this.nextthread++;
        this.scheduled_threads.write(nt);
        return nt;
    }
    
    public void setPlayerPosition(float x, float y)
    {
        this.vmdata[0] = x;
        this.vmdata[1] = y;
        return;
    }
    
    public int getThreadParent(int threadid)
    {
        return (int)(this.threads.get(threadid).threadvars[0]);
    }
    
    public ArrayList<Integer> getThreadChildren(int threadid)
    {
        return this.threads.get(threadid).children;
    }
    
    public float getState(int threadid, String state)
    {
        return this.threads.get(threadid).state[this.statename.get(state)];
    }
    
    public Iterator<Integer> getThreadIDs()
    {
        //int[] retval = new int[this.threads.size()];
        Set<Integer> s = this.threads.keySet();
        return s.iterator();
    }
    
    private IntQueue scheduled_threads = new IntQueue();
    
    public void run()
    {
        Iterator<Integer> it = this.getThreadIDs();
        while(it.hasNext())
        {
           int tid = it.next();
        	 ShooterThread th = threads.get(tid);
        	 if (!th.msg_isWaitingForMessage)
        	    scheduled_threads.write(tid);
        }
        while(true)
        {
            int tid = scheduled_threads.read();
            if (tid == IntQueue.NO_SUCH_ELEMENT)
               break;
            ShooterThread ct = this.threads.get(tid);
            while (ct.sleep <= 0)
            {
                if (ct.msg_isWaitingForMessage)
                   break;
                ct.codeloc = this.block2FuncCall(ct);
            }
            ct.sleep -= 1;
        }
        return;
    }
   
   private boolean recvwait(ShooterThread th, float msgtype)
   {
      if (!getMessage(th, msgtype))
      {
         th.msg_isWaitingForMessage = true;
         return false;
      }
      th.msg_isWaitingForMessage = false;
      return true;
   }
   
   /**
    * Send a message to the given thread from the given sending thread.
    *
    * This method is safe to call in instructions executed during run()
    * and is also safe to call outside of run() to generate external events.
    * If th_sender is null then a sending thread ID of -1 will be passed.
    */
   public void sendMessage(float msgtype, float msgdata, ShooterThread th_sender, float id_target)
   {
      float id_sender = (th_sender == null) ? -1 : (float) th_sender.threadvars[1];
      ShooterThread th_target = threads.get((int) id_target);
      sendMessageImpl(msgtype, msgdata, id_sender, th_target);
      if (!th_target.msg_isWaitingForMessage)
         return;
      scheduled_threads.write((int) th_target.threadvars[1]);
      th_target.msg_isWaitingForMessage = false;
      return;
   }
   
   private void sendMessageImpl(float msgtype, float msgdata, float id_sender, ShooterThread th_target)
   {
      Map<Integer, FloatQueue> m = th_target.msg_queue_map;
      FloatQueue q;
      if (m != null)
      {
         q = m.get((int) msgtype);
         if (q == null)
            return;    // silently discard unexpected messages for threads using message declarations
      }
      else
         q = th_target.msg_queue_all;
      q.write(msgtype);
      q.write(msgdata);
      q.write(id_sender);
      return;
   }
   
   public void declareMessage(ShooterThread th, float msgtype)
   {
       if (th.msg_queue_map == null)
          th.msg_queue_map = new TreeMap<Integer, FloatQueue>();
       int i = (int) msgtype;
       if (th.msg_queue_map.containsKey(i))
          return;
       FloatQueue q = new FloatQueue();
       th.msg_queue_map.put(i, q);
       separateMessages(th.msg_queue_all, q, (float) i);
       return;
   }
   
   public static void separateMessages(FloatQueue src, FloatQueue dest, float msgtype)
   {
      // Move all messages of given type from src to dest.
      int n = src.length();
      if ((n%3) != 0)
         throw(new IllegalStateException("Message queue length not divisible by 3"));
      for(int i=0;i<n;i+=3)
      {
         float itype    = src.read();
         float idata    = src.read();
         float isender  = src.read();
         FloatQueue q = (itype == msgtype) ? dest : src;
         q.write(itype);
         q.write(idata);
         q.write(isender);
      }
      return;
   }
   
   public boolean getMessage(ShooterThread th, float msgtype)
   {
      if (th.msg_queue_map == null)
      {
         FloatQueue q = th.msg_queue_all;
         if (q.isEmpty())
            return false;
         if (msgtype == -1)
         {
            this.tf1 = q.read();
            this.tf2 = q.read();
            this.tf3 = q.read();
            return true;
         }
         throw(new IllegalStateException("If you want to filter messages, use message declarations!"));
         // to implement this, you would pull messages from q until done or you get a message of the correct type
         // then put the irrelevant messages back
      }
      if (msgtype == -1)
      {
         for(FloatQueue q : th.msg_queue_map.values())
         {
            if (!q.isEmpty())
            {
               this.tf1 = q.read();
               this.tf2 = q.read();
               this.tf3 = q.read();
               return true;
            }
         }
         return false;
      }
      FloatQueue q = th.msg_queue_map.get((int) msgtype);
      if ((q == null) || (q.isEmpty()))
         return false;
      this.tf1 = q.read();
      this.tf2 = q.read();
      this.tf3 = q.read();
      return true;
   }
   
   public static String showFloat(float f)
   {
      int i = (int) f;
      return (f == (float) i) ? ""+i : ""+f;
   }
   
   public boolean isDone()
   {
      return (this.threads.size() == 0);
   }
   
    private int f0(ShooterThread sthread)
    {
        //mov;
        sthread.registers[10] = 200.0f;
      return this.f1(sthread);
    }
    
    private int f1(ShooterThread sthread)
    {
    float temp_tv2 = sthread.threadvars[2];
    float temp_register10 = sthread.registers[10];
        //sub;
        temp_register10 = temp_register10 - 1.0f;
        //cmp;
        temp_tv2 = (temp_register10 > 0.0f) ? 1f : 0f;
        //cndjmp
        if (temp_tv2 == 1)
        {
    sthread.registers[10] = temp_register10;
    sthread.threadvars[2] = temp_tv2;
           return this.f2(sthread);
        }
        //mov;
        temp_register10 = 200.0f;
        //jmp;
    sthread.registers[10] = temp_register10;
    sthread.threadvars[2] = temp_tv2;
        return this.f5(sthread);
    }
    
    private int f2(ShooterThread sthread)
    {
        //call;
        sthread.codetop++;
        sthread.codestack[sthread.codetop] = 3;
        return f16(sthread);
    }
    
    private int f3(ShooterThread sthread)
    {
        //mov;
        sthread.state[16] = sthread.state[0];
        //mov;
        sthread.state[17] = sthread.state[1];
        //halt;
        sthread.sleep = (int)(1.0f);
        return 4;
    }
    
    private int f4(ShooterThread sthread)
    {
        //jmp;
        return this.f1(sthread);
    }
    
    private int f5(ShooterThread sthread)
    {
        //mov;
        sthread.registers[2] = 0.0f;
      return this.f6(sthread);
    }
    
    private int f6(ShooterThread sthread)
    {
    float temp_tv2 = sthread.threadvars[2];
    float temp_tv1 = sthread.threadvars[1];
    float temp_register2 = sthread.registers[2];
        //cmp;
        temp_tv2 = (temp_register2 >= sthread.children.size()) ? 1f : 0f;
        //cndjmp
        if (temp_tv2 == 1)
        {
    sthread.registers[2] = temp_register2;
    sthread.threadvars[2] = temp_tv2;
    sthread.threadvars[1] = temp_tv1;
           return this.f8(sthread);
        }
        //cid;
        sthread.registers[1] = this.threads.get((int)(temp_tv1)).children.get((int)(temp_register2));
        //call;
        sthread.codetop++;
        sthread.codestack[sthread.codetop] = 7;
    sthread.registers[2] = temp_register2;
    sthread.threadvars[2] = temp_tv2;
    sthread.threadvars[1] = temp_tv1;
        return f14(sthread);
    }
    
    private int f7(ShooterThread sthread)
    {
    float temp_register2 = sthread.registers[2];
        //add;
        temp_register2 = temp_register2 + 1.0f;
        //jmp;
    sthread.registers[2] = temp_register2;
        return this.f6(sthread);
    }
    
    private int f8(ShooterThread sthread)
    {
        //mov;
        sthread.state[16] = sthread.state[0];
        //mov;
        sthread.state[17] = sthread.state[1];
        //halt;
        sthread.sleep = (int)(100.0f);
        return 9;
    }
    
    private int f9(ShooterThread sthread)
    {
        //mov;
        sthread.registers[2] = 0.0f;
      return this.f10(sthread);
    }
    
    private int f10(ShooterThread sthread)
    {
    float temp_tv2 = sthread.threadvars[2];
    float temp_tv1 = sthread.threadvars[1];
    float temp_register2 = sthread.registers[2];
        //cmp;
        temp_tv2 = (temp_register2 >= sthread.children.size()) ? 1f : 0f;
        //cndjmp
        if (temp_tv2 == 1)
        {
    sthread.registers[2] = temp_register2;
    sthread.threadvars[2] = temp_tv2;
    sthread.threadvars[1] = temp_tv1;
           return this.f12(sthread);
        }
        //cid;
        sthread.registers[1] = this.threads.get((int)(temp_tv1)).children.get((int)(temp_register2));
        //call;
        sthread.codetop++;
        sthread.codestack[sthread.codetop] = 11;
    sthread.registers[2] = temp_register2;
    sthread.threadvars[2] = temp_tv2;
    sthread.threadvars[1] = temp_tv1;
        return f15(sthread);
    }
    
    private int f11(ShooterThread sthread)
    {
    float temp_register2 = sthread.registers[2];
        //add;
        temp_register2 = temp_register2 + 1.0f;
        //jmp;
    sthread.registers[2] = temp_register2;
        return this.f10(sthread);
    }
    
    private int f12(ShooterThread sthread)
    {
        //mov;
        sthread.state[16] = sthread.state[0];
        //mov;
        sthread.state[17] = sthread.state[1];
        //halt;
        sthread.sleep = (int)(200.0f);
        return 13;
    }
    
    private int f13(ShooterThread sthread)
    {
        //jmp;
        return this.f1(sthread);
    }
    
    private int f14(ShooterThread sthread)
    {
    float temp_register1 = sthread.registers[1];
        //stv;
        this.threads.get((int)(temp_register1)).registers[0] = 1.0f;
        //ret;
        this.ti1 = sthread.codestack[sthread.codetop];
        sthread.threadvars[3] = 0.0f;
        sthread.codetop--;
    sthread.registers[1] = temp_register1;
        return this.ti1;
    }
    
    private int f15(ShooterThread sthread)
    {
    float temp_register1 = sthread.registers[1];
        //stv;
        this.threads.get((int)(temp_register1)).registers[1] = 1.0f;
        //ret;
        this.ti1 = sthread.codestack[sthread.codetop];
        sthread.threadvars[3] = 0.0f;
        sthread.codetop--;
    sthread.registers[1] = temp_register1;
        return this.ti1;
    }
    
    private int f16(ShooterThread sthread)
    {
    float temp_state2 = sthread.state[2];
        //rnd;
        temp_state2 = this.r.nextFloat();
        //mul;
        temp_state2 = temp_state2 * 6.28318531f;
        //call;
        sthread.codetop++;
        sthread.codestack[sthread.codetop] = 17;
    sthread.state[2] = temp_state2;
        return f35(sthread);
    }
    
    private int f17(ShooterThread sthread)
    {
    float temp_tv4 = sthread.threadvars[4];
    float temp_tv1 = sthread.threadvars[1];
    float temp_state4 = sthread.state[4];
    float temp_state3 = sthread.state[3];
    float temp_state2 = sthread.state[2];
    float temp_register1 = sthread.registers[1];
        //spawn;
        this.ti1 = (int)(temp_tv1);
        this.ti2 = this.spawnThread(20, 0, 0, 0, this.ti1);
        temp_tv4 = (float)(this.ti2);
        //stv;
        this.threads.get((int)(temp_tv4)).state[0] = temp_state3;
        //stv;
        this.threads.get((int)(temp_tv4)).state[1] = temp_state4;
        //stv;
        this.threads.get((int)(temp_tv4)).state[2] = temp_state2;
        //rnd;
        temp_register1 = this.r.nextFloat();
        //mul;
        temp_register1 = temp_register1 * 3.0f;
        //add;
        temp_register1 = temp_register1 + 2.0f;
        //stv;
        this.threads.get((int)(temp_tv4)).state[18] = temp_register1;
        //rnd;
        temp_state2 = this.r.nextFloat();
        //mul;
        temp_state2 = temp_state2 * 6.28318531f;
        //call;
        sthread.codetop++;
        sthread.codestack[sthread.codetop] = 18;
    sthread.registers[1] = temp_register1;
    sthread.state[4] = temp_state4;
    sthread.state[3] = temp_state3;
    sthread.state[2] = temp_state2;
    sthread.threadvars[4] = temp_tv4;
    sthread.threadvars[1] = temp_tv1;
        return f35(sthread);
    }
    
    private int f18(ShooterThread sthread)
    {
    float temp_tv4 = sthread.threadvars[4];
    float temp_tv1 = sthread.threadvars[1];
    float temp_state4 = sthread.state[4];
    float temp_state3 = sthread.state[3];
    float temp_state2 = sthread.state[2];
    float temp_register1 = sthread.registers[1];
        //spawn;
        this.ti1 = (int)(temp_tv1);
        this.ti2 = this.spawnThread(20, 0, 0, 0, this.ti1);
        temp_tv4 = (float)(this.ti2);
        //stv;
        this.threads.get((int)(temp_tv4)).state[0] = temp_state3;
        //stv;
        this.threads.get((int)(temp_tv4)).state[1] = temp_state4;
        //stv;
        this.threads.get((int)(temp_tv4)).state[2] = temp_state2;
        //rnd;
        temp_register1 = this.r.nextFloat();
        //mul;
        temp_register1 = temp_register1 * 3.0f;
        //add;
        temp_register1 = temp_register1 + 2.0f;
        //stv;
        this.threads.get((int)(temp_tv4)).state[18] = temp_register1;
        //rnd;
        temp_state2 = this.r.nextFloat();
        //mul;
        temp_state2 = temp_state2 * 6.28318531f;
        //call;
        sthread.codetop++;
        sthread.codestack[sthread.codetop] = 19;
    sthread.registers[1] = temp_register1;
    sthread.state[4] = temp_state4;
    sthread.state[3] = temp_state3;
    sthread.state[2] = temp_state2;
    sthread.threadvars[4] = temp_tv4;
    sthread.threadvars[1] = temp_tv1;
        return f35(sthread);
    }
    
    private int f19(ShooterThread sthread)
    {
    float temp_tv4 = sthread.threadvars[4];
    float temp_tv1 = sthread.threadvars[1];
    float temp_state4 = sthread.state[4];
    float temp_state3 = sthread.state[3];
    float temp_state2 = sthread.state[2];
    float temp_register1 = sthread.registers[1];
        //spawn;
        this.ti1 = (int)(temp_tv1);
        this.ti2 = this.spawnThread(20, 0, 0, 0, this.ti1);
        temp_tv4 = (float)(this.ti2);
        //stv;
        this.threads.get((int)(temp_tv4)).state[0] = temp_state3;
        //stv;
        this.threads.get((int)(temp_tv4)).state[1] = temp_state4;
        //stv;
        this.threads.get((int)(temp_tv4)).state[2] = temp_state2;
        //rnd;
        temp_register1 = this.r.nextFloat();
        //mul;
        temp_register1 = temp_register1 * 3.0f;
        //add;
        temp_register1 = temp_register1 + 2.0f;
        //stv;
        this.threads.get((int)(temp_tv4)).state[18] = temp_register1;
        //ret;
        this.ti1 = sthread.codestack[sthread.codetop];
        sthread.threadvars[3] = 0.0f;
        sthread.codetop--;
    sthread.registers[1] = temp_register1;
    sthread.state[4] = temp_state4;
    sthread.state[3] = temp_state3;
    sthread.state[2] = temp_state2;
    sthread.threadvars[4] = temp_tv4;
    sthread.threadvars[1] = temp_tv1;
        return this.ti1;
    }
    
    private int f20(ShooterThread sthread)
    {
        //mov;
        sthread.registers[2] = 200.0f;
      return this.f21(sthread);
    }
    
    private int f21(ShooterThread sthread)
    {
    float temp_tv2 = sthread.threadvars[2];
    float temp_register0 = sthread.registers[0];
        //cmp;
        temp_tv2 = (temp_register0 == 1.0f) ? 1f : 0f;
        //cndjmp
        if (temp_tv2 == 1)
        {
    sthread.registers[0] = temp_register0;
    sthread.threadvars[2] = temp_tv2;
           return this.f24(sthread);
        }
        //call;
        sthread.codetop++;
        sthread.codestack[sthread.codetop] = 22;
    sthread.registers[0] = temp_register0;
    sthread.threadvars[2] = temp_tv2;
        return f33(sthread);
    }
    
    private int f22(ShooterThread sthread)
    {
        //mov;
        sthread.state[16] = sthread.state[0];
        //mov;
        sthread.state[17] = sthread.state[1];
        //halt;
        sthread.sleep = (int)(1.0f);
        return 23;
    }
    
    private int f23(ShooterThread sthread)
    {
        //jmp;
        return this.f21(sthread);
    }
    
    private int f24(ShooterThread sthread)
    {
        //mov;
        sthread.state[18] = 0.0f;
      return this.f25(sthread);
    }
    
    private int f25(ShooterThread sthread)
    {
    float temp_tv2 = sthread.threadvars[2];
    float temp_register1 = sthread.registers[1];
        //cmp;
        temp_tv2 = (temp_register1 == 1.0f) ? 1f : 0f;
        //cndjmp
        if (temp_tv2 == 1)
        {
    sthread.registers[1] = temp_register1;
    sthread.threadvars[2] = temp_tv2;
           return this.f27(sthread);
        }
        //mov;
        sthread.state[16] = sthread.state[0];
        //mov;
        sthread.state[17] = sthread.state[1];
        //halt;
        sthread.sleep = (int)(1.0f);
    sthread.registers[1] = temp_register1;
    sthread.threadvars[2] = temp_tv2;
        return 26;
    }
    
    private int f26(ShooterThread sthread)
    {
        //jmp;
        return this.f25(sthread);
    }
    
    private int f27(ShooterThread sthread)
    {
    float temp_state2 = sthread.state[2];
        //rnd;
        temp_state2 = this.r.nextFloat();
        //mul;
        temp_state2 = temp_state2 * 6.28318531f;
        //mov;
        sthread.state[19] = 0.02f;
    sthread.state[2] = temp_state2;
      return this.f28(sthread);
    }
    
    private int f28(ShooterThread sthread)
    {
    float temp_tv2 = sthread.threadvars[2];
    float temp_register2 = sthread.registers[2];
        //sub;
        temp_register2 = temp_register2 - 1.0f;
        //cmp;
        temp_tv2 = (temp_register2 > 0.0f) ? 1f : 0f;
        //cndjmp
        if (temp_tv2 == 1)
        {
    sthread.registers[2] = temp_register2;
    sthread.threadvars[2] = temp_tv2;
           return this.f29(sthread);
        }
        //mov;
        temp_register2 = 200.0f;
        //jmp;
    sthread.registers[2] = temp_register2;
    sthread.threadvars[2] = temp_tv2;
        return this.f32(sthread);
    }
    
    private int f29(ShooterThread sthread)
    {
        //call;
        sthread.codetop++;
        sthread.codestack[sthread.codetop] = 30;
        return f33(sthread);
    }
    
    private int f30(ShooterThread sthread)
    {
        //mov;
        sthread.state[16] = sthread.state[0];
        //mov;
        sthread.state[17] = sthread.state[1];
        //halt;
        sthread.sleep = (int)(1.0f);
        return 31;
    }
    
    private int f31(ShooterThread sthread)
    {
        //jmp;
        return this.f28(sthread);
    }
    
    private int f32(ShooterThread sthread)
    {
    float temp_tv0 = sthread.threadvars[0];
    float temp_tv1 = sthread.threadvars[1];
        //terminate
        this.ti1 = (int)(temp_tv1);
        if (temp_tv0 >= 0.0f)
        {
            this.ti2 = this.threads.get((int)(temp_tv0)).children.indexOf((int)ti1);
            this.threads.get((int)(temp_tv0)).children.remove(ti2);
        }
        for (int i = 0; i < sthread.children.size(); i++)
        {
            this.ti2 = sthread.children.get(i).intValue();
            this.threads.get(this.ti2).threadvars[0] = -1;
        }
        this.threads.remove(this.ti1);
        sthread.threadvars[6] = 1.0f;
        sthread.sleep = 1;
        this.ready_threads.push(sthread);
    sthread.threadvars[0] = temp_tv0;
    sthread.threadvars[1] = temp_tv1;
        return 0;
    }
    
    private int f33(ShooterThread sthread)
    {
    float temp_tv2 = sthread.threadvars[2];
    float temp_tv9 = sthread.threadvars[9];
    float temp_state20 = sthread.state[20];
    float temp_state18 = sthread.state[18];
    float temp_state21 = sthread.state[21];
    float temp_state23 = sthread.state[23];
    float temp_state7 = sthread.state[7];
    float temp_state0 = sthread.state[0];
    float temp_state2 = sthread.state[2];
    float temp_state25 = sthread.state[25];
    float temp_state1 = sthread.state[1];
    float temp_state8 = sthread.state[8];
    float temp_register2 = sthread.registers[2];
    float temp_register3 = sthread.registers[3];
    float temp_register0 = sthread.registers[0];
    float temp_register4 = sthread.registers[4];
    float temp_register5 = sthread.registers[5];
    float temp_register1 = sthread.registers[1];
    float temp_register6 = sthread.registers[6];
        //push;
        temp_tv9+=1.0f;
        sthread.varstack[(int)(temp_tv9)] = temp_register0;
        //push;
        temp_tv9+=1.0f;
        sthread.varstack[(int)(temp_tv9)] = temp_register1;
        //push;
        temp_tv9+=1.0f;
        sthread.varstack[(int)(temp_tv9)] = temp_register2;
        //push;
        temp_tv9+=1.0f;
        sthread.varstack[(int)(temp_tv9)] = temp_register3;
        //push;
        temp_tv9+=1.0f;
        sthread.varstack[(int)(temp_tv9)] = temp_register4;
        //push;
        temp_tv9+=1.0f;
        sthread.varstack[(int)(temp_tv9)] = temp_register5;
        //push;
        temp_tv9+=1.0f;
        sthread.varstack[(int)(temp_tv9)] = temp_register6;
        //add;
        temp_state7 = temp_state7 + sthread.state[9];
        //add;
        temp_state8 = temp_state8 + sthread.state[10];
        //add;
        temp_state0 = temp_state0 + temp_state7;
        //add;
        temp_state1 = temp_state1 + temp_state8;
        //add;
        temp_state18 = temp_state18 + sthread.state[19];
        //cos;
        temp_register0 = (float)(Math.cos(temp_state2));
        //mul;
        temp_register0 = temp_register0 * temp_state18;
        //add;
        temp_state0 = temp_state0 + temp_register0;
        //sin;
        temp_register0 = (float)(Math.sin(temp_state2));
        //mul;
        temp_register0 = temp_register0 * temp_state18;
        //add;
        temp_state1 = temp_state1 + temp_register0;
        //add;
        temp_state25 = temp_state25 + sthread.state[26];
        //add;
        temp_state2 = temp_state2 + temp_state25;
        //add;
        temp_state21 = temp_state21 + sthread.state[22];
        //add;
        temp_state23 = temp_state23 + sthread.state[24];
        //sub;
        temp_register0 = temp_state0 - sthread.state[3];
        //sub;
        temp_register1 = temp_state1 - sthread.state[4];
        //mul;
        temp_register0 = temp_register0 * temp_register0;
        //mul;
        temp_register1 = temp_register1 * temp_register1;
        //add;
        temp_register0 = temp_register0 + temp_register1;
        //sqrt;
        temp_register2 = (float)(Math.sqrt(temp_register0));
        //mov;
        temp_register3 = temp_state21;
        //cmp;
        temp_tv2 = (temp_state20 == 1.0f) ? 1f : 0f;
        //cndjmp
        if (temp_tv2 == 1)
        {
    sthread.registers[2] = temp_register2;
    sthread.registers[3] = temp_register3;
    sthread.registers[0] = temp_register0;
    sthread.registers[4] = temp_register4;
    sthread.registers[5] = temp_register5;
    sthread.registers[1] = temp_register1;
    sthread.registers[6] = temp_register6;
    sthread.state[20] = temp_state20;
    sthread.state[18] = temp_state18;
    sthread.state[21] = temp_state21;
    sthread.state[23] = temp_state23;
    sthread.state[7] = temp_state7;
    sthread.state[0] = temp_state0;
    sthread.state[2] = temp_state2;
    sthread.state[25] = temp_state25;
    sthread.state[1] = temp_state1;
    sthread.state[8] = temp_state8;
    sthread.threadvars[2] = temp_tv2;
    sthread.threadvars[9] = temp_tv9;
           return this.f34(sthread);
        }
        //div;
        temp_register3 = temp_register3 / temp_register2;
    sthread.registers[2] = temp_register2;
    sthread.registers[3] = temp_register3;
    sthread.registers[0] = temp_register0;
    sthread.registers[4] = temp_register4;
    sthread.registers[5] = temp_register5;
    sthread.registers[1] = temp_register1;
    sthread.registers[6] = temp_register6;
    sthread.state[20] = temp_state20;
    sthread.state[18] = temp_state18;
    sthread.state[21] = temp_state21;
    sthread.state[23] = temp_state23;
    sthread.state[7] = temp_state7;
    sthread.state[0] = temp_state0;
    sthread.state[2] = temp_state2;
    sthread.state[25] = temp_state25;
    sthread.state[1] = temp_state1;
    sthread.state[8] = temp_state8;
    sthread.threadvars[2] = temp_tv2;
    sthread.threadvars[9] = temp_tv9;
      return this.f34(sthread);
    }
    
    private int f34(ShooterThread sthread)
    {
    float temp_tv9 = sthread.threadvars[9];
    float temp_state4 = sthread.state[4];
    float temp_state23 = sthread.state[23];
    float temp_state1 = sthread.state[1];
    float temp_state0 = sthread.state[0];
    float temp_state3 = sthread.state[3];
    float temp_register2 = sthread.registers[2];
    float temp_register3 = sthread.registers[3];
    float temp_register0 = sthread.registers[0];
    float temp_register4 = sthread.registers[4];
    float temp_register5 = sthread.registers[5];
    float temp_register1 = sthread.registers[1];
    float temp_register6 = sthread.registers[6];
        //cos;
        temp_register4 = (float)(Math.cos(temp_register3));
        //sin;
        temp_register3 = (float)(Math.sin(temp_register3));
        //sub;
        temp_register0 = temp_state0 - temp_state3;
        //sub;
        temp_register1 = temp_state1 - temp_state4;
        //mul;
        temp_register5 = temp_register4 * temp_register0;
        //mul;
        temp_register6 = temp_register3 * temp_register1;
        //sub;
        temp_register5 = temp_register5 - temp_register6;
        //add;
        temp_state0 = temp_state3 + temp_register5;
        //mul;
        temp_register5 = temp_register3 * temp_register0;
        //mul;
        temp_register6 = temp_register4 * temp_register1;
        //add;
        temp_register5 = temp_register5 + temp_register6;
        //add;
        temp_state1 = temp_state4 + temp_register5;
        //div;
        temp_register2 = 1.0f / temp_register2;
        //mul;
        temp_register0 = temp_register0 * temp_state23;
        //mul;
        temp_register0 = temp_register0 * temp_register2;
        //add;
        temp_state0 = temp_state0 + temp_register0;
        //mul;
        temp_register1 = temp_register1 * temp_state23;
        //mul;
        temp_register1 = temp_register1 * temp_register2;
        //add;
        temp_state1 = temp_state1 + temp_register1;
        //pop;
        temp_register6 = sthread.varstack[(int)(temp_tv9)];
        temp_tv9-=1.0f;
        //pop;
        temp_register5 = sthread.varstack[(int)(temp_tv9)];
        temp_tv9-=1.0f;
        //pop;
        temp_register4 = sthread.varstack[(int)(temp_tv9)];
        temp_tv9-=1.0f;
        //pop;
        temp_register3 = sthread.varstack[(int)(temp_tv9)];
        temp_tv9-=1.0f;
        //pop;
        temp_register2 = sthread.varstack[(int)(temp_tv9)];
        temp_tv9-=1.0f;
        //pop;
        temp_register1 = sthread.varstack[(int)(temp_tv9)];
        temp_tv9-=1.0f;
        //pop;
        temp_register0 = sthread.varstack[(int)(temp_tv9)];
        temp_tv9-=1.0f;
        //ret;
        this.ti1 = sthread.codestack[sthread.codetop];
        sthread.threadvars[3] = 0.0f;
        sthread.codetop--;
    sthread.registers[2] = temp_register2;
    sthread.registers[3] = temp_register3;
    sthread.registers[0] = temp_register0;
    sthread.registers[4] = temp_register4;
    sthread.registers[5] = temp_register5;
    sthread.registers[1] = temp_register1;
    sthread.registers[6] = temp_register6;
    sthread.state[4] = temp_state4;
    sthread.state[23] = temp_state23;
    sthread.state[1] = temp_state1;
    sthread.state[0] = temp_state0;
    sthread.state[3] = temp_state3;
    sthread.threadvars[9] = temp_tv9;
        return this.ti1;
    }
    
    private int f35(ShooterThread sthread)
    {
        //mov;
        sthread.state[3] = sthread.state[0];
        //mov;
        sthread.state[4] = sthread.state[1];
        //ret;
        this.ti1 = sthread.codestack[sthread.codetop];
        sthread.threadvars[3] = 0.0f;
        sthread.codetop--;
        return this.ti1;
    }
    
    private int f36(ShooterThread sthread)
    {
    float temp_tv0 = sthread.threadvars[0];
        //gtv;
        sthread.state[3] = this.threads.get((int)(temp_tv0)).state[0];
        //gtv;
        sthread.state[4] = this.threads.get((int)(temp_tv0)).state[1];
        //ret;
        this.ti1 = sthread.codestack[sthread.codetop];
        sthread.threadvars[3] = 0.0f;
        sthread.codetop--;
    sthread.threadvars[0] = temp_tv0;
        return this.ti1;
    }
    
    private int f37(ShooterThread sthread)
    {
    float temp_tv2 = sthread.threadvars[2];
    float temp_tv9 = sthread.threadvars[9];
    float temp_mem1 = this.mem[1];
    float temp_register1 = sthread.registers[1];
    float temp_register2 = sthread.registers[2];
    float temp_register3 = sthread.registers[3];
    float temp_register0 = sthread.registers[0];
        //sub;
        temp_register3 = temp_register3 - 1.0f;
        //cmp;
        temp_tv2 = (temp_register3 < 0.0f) ? 1f : 0f;
        //cndjmp
        if (temp_tv2 == 1)
        {
    sthread.registers[1] = temp_register1;
    sthread.registers[2] = temp_register2;
    sthread.registers[3] = temp_register3;
    sthread.registers[0] = temp_register0;
    this.mem[1] = temp_mem1;
    sthread.threadvars[2] = temp_tv2;
    sthread.threadvars[9] = temp_tv9;
           return this.f38(sthread);
        }
        //push;
        temp_tv9+=1.0f;
        sthread.varstack[(int)(temp_tv9)] = temp_register0;
        //cid;
        temp_register0 = this.threads.get((int)(temp_register0)).children.get((int)(temp_register3));
        //push;
        temp_tv9+=1.0f;
        sthread.varstack[(int)(temp_tv9)] = temp_mem1;
        //gtv;
        temp_mem1 = this.threads.get((int)(temp_register0)).state[0];
        //add;
        temp_mem1 = temp_mem1 + temp_register1;
        //stv;
        this.threads.get((int)(temp_register0)).state[0] = temp_mem1;
        //gtv;
        temp_mem1 = this.threads.get((int)(temp_register0)).state[1];
        //add;
        temp_mem1 = temp_mem1 + temp_register2;
        //stv;
        this.threads.get((int)(temp_register0)).state[1] = temp_mem1;
        //pop;
        temp_mem1 = sthread.varstack[(int)(temp_tv9)];
        temp_tv9-=1.0f;
        //pop;
        temp_register0 = sthread.varstack[(int)(temp_tv9)];
        temp_tv9-=1.0f;
        //jmp;
    sthread.registers[1] = temp_register1;
    sthread.registers[2] = temp_register2;
    sthread.registers[3] = temp_register3;
    sthread.registers[0] = temp_register0;
    this.mem[1] = temp_mem1;
    sthread.threadvars[2] = temp_tv2;
    sthread.threadvars[9] = temp_tv9;
        return this.f37(sthread);
    }
    
    private int f38(ShooterThread sthread)
    {
    float temp_tv9 = sthread.threadvars[9];
        //pop;
        sthread.registers[3] = sthread.varstack[(int)(temp_tv9)];
        temp_tv9-=1.0f;
        //ret;
        this.ti1 = sthread.codestack[sthread.codetop];
        sthread.threadvars[3] = 0.0f;
        sthread.codetop--;
    sthread.threadvars[9] = temp_tv9;
        return this.ti1;
    }
    
}
