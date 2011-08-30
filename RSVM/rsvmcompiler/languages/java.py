def constructOutputFiles(code, fname="gen.java"):
    bp = __getBoilerPlateFiles()
    gen = __constructMainFile(code, fname)
    return bp.update(gen)

def fromString(string):
    return None

def optimize(code, options={}):
    return

def __constructMainFile(code, fname):
    ucode = code[1]
    outdic={}
    ent=[]
    #append the first part of the boilerplate code
    ent += bp_1
    
    #append the switch statement code
    for i in range(len(ucode)):
        ent.append("           case "+str(i)+": retval = this.f"+str(i)+"(th); break;")
    
    #append the second part of the boilerplate code
    ent += bp_2
    
    #append the generated code
    for i, block in enumerate(ucode):
        ent.append("    private int f"+str(i)+"(ShooterThread sthread)")
        ent.append("    {")
        ent += block
    
    outdic[fname] = ent
    return outdic

def __getBoilerPlateFiles():
    return {"EventHandler.java":bp_EventHandler, "FloatQueue.java":bp_FloatQueue, "IntQueue.java":bp_IntQueue, "ShooterThread.java":bp_ShooterThread, "ShooterVirtualMachine.java":bp_ShooterVirtualMachine}

def __repr__():
    return "java"

bp_EventHandler='/**\n\
 *\n\
 * An EventHandler receives events from other VM threads or from the system.\n\
 *\n\
 * An event has a channel, and three data fields.  The data fields are visible\n\
 * to the program, but the channel is used solely by the runtime.\n\
 *\n\
 * A channel can be regarded as equivalent to an IRQ in hardware programming,\n\
 * that is, it identifies the specific source of the event.  The sender is the\n\
 * ID of the sending thread, while type and data are used by the application.\n\
 *\n\
 * (Type is actually used by the filter mechanism to implement postponing\n\
 * uninteresting messages.)\n\
 */\n\
\n\
public interface EventHandler\n\
{\n\
    public void handleEvent(int channel, float sender, float type, float data);\n\
}'.split("\n")
    
bp_FloatQueue='public class FloatQueue\n\
{\n\
   float buffer[];\n\
   int bread, bwrite;\n\
\n\
   public FloatQueue()\n\
   {\n\
      this.buffer = new float[8];\n\
      this.bread = 0;\n\
      this.bwrite = 0;\n\
      return;\n\
   }\n\
\n\
   public static final float NO_SUCH_ELEMENT = Float.NaN;\n\
\n\
   public float read()\n\
   {\n\
      if (bread == bwrite)\n\
         return NO_SUCH_ELEMENT;\n\
      float result = buffer[bread++];\n\
      if (bread >= buffer.length)\n\
         bread -= buffer.length;\n\
      return result;\n\
   }\n\
\n\
   public void write(float x)\n\
   {\n\
      buffer[bwrite++] = x;\n\
      if (bwrite >= buffer.length)\n\
         bwrite -= buffer.length;\n\
      if (bwrite == bread)\n\
      {\n\
         float temp[] = new float[buffer.length*2];\n\
         System.arraycopy(buffer, bread, temp, 0, buffer.length-bread);\n\
         System.arraycopy(buffer, 0, temp, buffer.length-bread, bread);\n\
         bread = 0;\n\
         bwrite = buffer.length;\n\
         buffer = temp;\n\
      }\n\
      return;\n\
   }\n\
\n\
   public boolean isEmpty()\n\
   {\n\
      return (bwrite == bread);\n\
   }\n\
\n\
   public float[] toArray()\n\
   {\n\
      float result[];\n\
      if (bwrite < bread)\n\
      {\n\
         result = new float[buffer.length-bread+bwrite];\n\
         System.arraycopy(buffer, bread, result, 0, buffer.length-bread);\n\
         System.arraycopy(buffer, 0, result, buffer.length-bread, bwrite);\n\
      }\n\
      else\n\
      {\n\
         result = new float[bwrite-bread];\n\
         System.arraycopy(buffer, bread, result, 0, bwrite-bread);\n\
      }\n\
      return result;\n\
   }\n\
}'.split("\n")

bp_IntQueue='public class IntQueue\n\
{\n\
   int buffer[];\n\
   int bread, bwrite;\n\
\n\
   public IntQueue()\n\
   {\n\
      this.buffer = new int[8];\n\
      this.bread = 0;\n\
      this.bwrite = 0;\n\
      return;\n\
   }\n\
\n\
   public static final int NO_SUCH_ELEMENT = 0x80000000;\n\
\n\
   public int read()\n\
   {\n\
      if (bread == bwrite)\n\
         return NO_SUCH_ELEMENT;\n\
      int result = buffer[bread++];\n\
      if (bread >= buffer.length)\n\
         bread -= buffer.length;\n\
      return result;\n\
   }\n\
\n\
   public void write(int x)\n\
   {\n\
      buffer[bwrite++] = x;\n\
      if (bwrite >= buffer.length)\n\
         bwrite -= buffer.length;\n\
      if (bwrite == bread)\n\
      {\n\
         int temp[] = new int[buffer.length*2];\n\
         System.arraycopy(buffer, bread, temp, 0, buffer.length-bread);\n\
         System.arraycopy(buffer, 0, temp, buffer.length-bread, bread);\n\
         bread = 0;\n\
         bwrite = buffer.length;\n\
         buffer = temp;\n\
      }\n\
      return;\n\
   }\n\
\n\
   public boolean isEmpty()\n\
   {\n\
      return (bwrite == bread);\n\
   }\n\
\n\
   public int[] toArray()\n\
   {\n\
      int result[];\n\
      if (bwrite < bread)\n\
      {\n\
         result = new int[buffer.length-bread+bwrite];\n\
         System.arraycopy(buffer, bread, result, 0, buffer.length-bread);\n\
         System.arraycopy(buffer, 0, result, buffer.length-bread, bwrite);\n\
      }\n\
      else\n\
      {\n\
         result = new int[bwrite-bread];\n\
         System.arraycopy(buffer, bread, result, 0, bwrite-bread);\n\
      }\n\
      return result;\n\
   }\n\
}'.split("\n")

bp_ShooterThread='package com.youkaicountry.testrsvm;\n\
\n\
import java.util.ArrayList;\n\
\n\
public class ShooterThread\n\
{\n\
    public int codeloc = 0;\n\
    public float[] registers;\n\
    public float[] state = new float[30];\n\
    public int sleep = 0;\n\
    public ArrayList<Integer> children = new ArrayList<Integer>();\n\
    public ArrayList<Integer> codestack = new ArrayList<Integer>();\n\
    public ArrayList<Float> varstack = new ArrayList<Float>();\n\
    public float[] threadvars = new float[8];\n\
    \n\
    public ShooterThread(int codeloc, int regsize)\n\
    {\n\
        if (codeloc < 0)\n\
        {\n\
            this.codeloc = 0;\n\
        }\n\
        else\n\
        {\n\
            this.codeloc = codeloc;\n\
        }\n\
        \n\
        if (regsize < 0)\n\
        {\n\
            this.registers = new float[64];\n\
        }\n\
        else\n\
        {\n\
            this.registers = new float[regsize];\n\
        }\n\
        this.threadvars[0] = -1.0f;\n\
        \n\
    }\n\
}'.split("\n")

bp_ShooterVirtualMachine='package com.youkaicountry.testrsvm;\n\
\n\
import java.util.ArrayList;\n\
import java.util.Iterator;\n\
\n\
interface ShooterVirtualMachine\n\
{\n\
    Iterator getThreadIDs();\n\
    float getState(int threatid, String state);\n\
    ArrayList<Integer> getThreadChildren(int threadid);\n\
    int getThreadParent(int threadid);\n\
    void setPlayerPosition(float x, float y);\n\
    int spawnThread(int initloc, float x, float y, float angle, int parent);\n\
    void run();\n\
}'.split("\n")

bp_1='import java.util.ArrayList;\n\
import java.util.Hashtable;\n\
import java.util.Iterator;\n\
import java.util.Map;\n\
import java.util.Random;\n\
import java.util.Set;\n\
import java.util.Stack;\n\
import java.util.TreeMap;\n\
\n\
@SuppressWarnings("all")\n\
class RSVM implements ShooterVirtualMachine\n\
   {\n\
    public Hashtable<Integer, ShooterThread> threads;\n\
    public Hashtable<String, Integer> statename;\n\
    public float[] mem;\n\
    public Random r = null;\n\
    public float[] vmdata = new float[2];\n\
    public int regsize;\n\
    public int stacksize;\n\
    public int nextthread;\n\
    private float tf1, tf2, tf3;\n\
    private int ti1, ti2;\n\
    private Stack<ShooterThread> ready_threads;\n\
    \n\
    //try 64, 32, 32, 32, null\n\
    //if r is null, a new one is made.\n\
    public RSVM(int memsize, int regsize, int stacksize, int initthreads, Random r)\n\
    {\n\
        if (r == null) {this.r = new Random();}\n\
        this.ready_threads = new Stack<ShooterThread>();\n\
        for (int i = 0; i < initthreads; i++)\n\
        {\n\
            this.ready_threads.push(new ShooterThread(0, regsize, stacksize));\n\
        }\n\
        this.threads = new Hashtable<Integer, ShooterThread>();\n\
        this.mem = new float[memsize];\n\
        this.regsize = regsize;\n\
        this.stacksize = stacksize;\n\
        this.nextthread = 0;\n\
        this.mem[0] = 0;\n\
        this.mem[1] = 0;\n\
        this.statename = new Hashtable<String, Integer>();\n\
        statename.put("x", new Integer(0));\n\
        statename.put("__x", new Integer(0));\n\
        statename.put("y", new Integer(1));\n\
        statename.put("__y", new Integer(1));\n\
        statename.put("angle", new Integer(2));\n\
        statename.put("__angle", new Integer(2));\n\
        statename.put("targetx", new Integer(3));\n\
        statename.put("__targetx", new Integer(3));\n\
        statename.put("targety", new Integer(4));\n\
        statename.put("__targety", new Integer(4));\n\
        statename.put("returnval", new Integer(5));\n\
        statename.put("__returnval", new Integer(5));\n\
        statename.put("condition", new Integer(6));\n\
        statename.put("__condition", new Integer(6));\n\
        statename.put("sprite", new Integer(27));\n\
        statename.put("__sprite", new Integer(27));\n\
        statename.put("radius", new Integer(28));\n\
        statename.put("__radius", new Integer(28));\n\
        return;\n\
    }\n\
    \n\
    private int block2FuncCall(ShooterThread th)\n\
    {\n\
        int retval = 0;\n\
        switch (th.codeloc)\n\
        {'.split("\n")

bp_2='}\n\
        return retval;\n\
    }\n\
    \n\
    public int spawnThread(int initloc, float x, float y, float angle, int parent)\n\
    {\n\
        int nt = this.nextthread;\n\
        ShooterThread st;\n\
        if (this.ready_threads.empty())\n\
        {\n\
            st = new ShooterThread(initloc, this.regsize, this.stacksize);\n\
        }\n\
        else\n\
        {\n\
            st = (ShooterThread)(this.ready_threads.pop());\n\
            st.clear(initloc);\n\
        }\n\
        this.threads.put(nt, st);\n\
        st.state[0] = x;\n\
        st.state[1] = y;\n\
        st.state[2] = angle;\n\
        st.threadvars[1] = nt;\n\
        if (parent >= 0)\n\
        {\n\
            st.threadvars[0] = parent;\n\
            this.threads.get(parent).children.add(this.threads.get(parent).children.size(), nt);\n\
        }\n\
        else\n\
        {\n\
            st.threadvars[0] = -1;\n\
        }\n\
        this.nextthread++;\n\
        this.scheduled_threads.write(nt);\n\
        return nt;\n\
    }\n\
    \n\
    public void setPlayerPosition(float x, float y)\n\
    {\n\
        this.vmdata[0] = x;\n\
        this.vmdata[1] = y;\n\
        return;\n\
    }\n\
    \n\
    public int getThreadParent(int threadid)\n\
    {\n\
        return (int)(this.threads.get(threadid).threadvars[0]);\n\
    }\n\
    \n\
    public ArrayList<Integer> getThreadChildren(int threadid)\n\
    {\n\
        return this.threads.get(threadid).children;\n\
    }\n\
    \n\
    public float getState(int threadid, String state)\n\
    {\n\
        return this.threads.get(threadid).state[this.statename.get(state)];\n\
    }\n\
    \n\
    public Iterator<Integer> getThreadIDs()\n\
    {\n\
        //int[] retval = new int[this.threads.size()];\n\
        Set<Integer> s = this.threads.keySet();\n\
        return s.iterator();\n\
    }\n\
    \n\
    private IntQueue scheduled_threads = new IntQueue();\n\
    \n\
    public void run()\n\
    {\n\
        Iterator<Integer> it = this.getThreadIDs();\n\
        while(it.hasNext())\n\
        {\n\
           int tid = it.next();\n\
        	 ShooterThread th = threads.get(tid);\n\
        	 if (!th.msg_isWaitingForMessage)\n\
        	    scheduled_threads.write(tid);\n\
        }\n\
        while(true)\n\
        {\n\
            int tid = scheduled_threads.read();\n\
            if (tid == IntQueue.NO_SUCH_ELEMENT)\n\
               break;\n\
            ShooterThread ct = this.threads.get(tid);\n\
            while (ct.sleep <= 0)\n\
            {\n\
                if (ct.msg_isWaitingForMessage)\n\
                   break;\n\
                ct.codeloc = this.block2FuncCall(ct);\n\
            }\n\
            ct.sleep -= 1;\n\
        }\n\
        return;\n\
    }\n\
   \n\
   private boolean recvwait(ShooterThread th, float msgtype)\n\
   {\n\
      if (!getMessage(th, msgtype))\n\
      {\n\
         th.msg_isWaitingForMessage = true;\n\
         return false;\n\
      }\n\
      th.msg_isWaitingForMessage = false;\n\
      return true;\n\
   }\n\
   \n\
   /**\n\
    * Send a message to the given thread from the given sending thread.\n\
    *\n\
    * This method is safe to call in instructions executed during run()\n\
    * and is also safe to call outside of run() to generate external events.\n\
    * If th_sender is null then a sending thread ID of -1 will be passed.\n\
    */\n\
   public void sendMessage(float msgtype, float msgdata, ShooterThread th_sender, float id_target)\n\
   {\n\
      float id_sender = (th_sender == null) ? -1 : (float) th_sender.threadvars[1];\n\
      ShooterThread th_target = threads.get((int) id_target);\n\
      sendMessageImpl(msgtype, msgdata, id_sender, th_target);\n\
      if (!th_target.msg_isWaitingForMessage)\n\
         return;\n\
      scheduled_threads.write((int) th_target.threadvars[1]);\n\
      th_target.msg_isWaitingForMessage = false;\n\
      return;\n\
   }\n\
   \n\
   private void sendMessageImpl(float msgtype, float msgdata, float id_sender, ShooterThread th_target)\n\
   {\n\
      Map<Integer, FloatQueue> m = th_target.msg_queue_map;\n\
      FloatQueue q;\n\
      if (m != null)\n\
      {\n\
         q = m.get((int) msgtype);\n\
         if (q == null)\n\
            return;    // silently discard unexpected messages for threads using message declarations\n\
      }\n\
      else\n\
         q = th_target.msg_queue_all;\n\
      q.write(msgtype);\n\
      q.write(msgdata);\n\
      q.write(id_sender);\n\
      return;\n\
   }\n\
   \n\
   public void declareMessage(ShooterThread th, float msgtype)\n\
   {\n\
       if (th.msg_queue_map == null)\n\
          th.msg_queue_map = new TreeMap<Integer, FloatQueue>();\n\
       int i = (int) msgtype;\n\
       if (th.msg_queue_map.containsKey(i))\n\
          return;\n\
       FloatQueue q = new FloatQueue();\n\
       th.msg_queue_map.put(i, q);\n\
       separateMessages(th.msg_queue_all, q, (float) i);\n\
       return;\n\
   }\n\
   \n\
   public static void separateMessages(FloatQueue src, FloatQueue dest, float msgtype)\n\
   {\n\
      // Move all messages of given type from src to dest.\n\
      int n = src.length();\n\
      if ((n%3) != 0)\n\
         throw(new IllegalStateException("Message queue length not divisible by 3"));\n\
      for(int i=0;i<n;i+=3)\n\
      {\n\
         float itype    = src.read();\n\
         float idata    = src.read();\n\
         float isender  = src.read();\n\
         FloatQueue q = (itype == msgtype) ? dest : src;\n\
         q.write(itype);\n\
         q.write(idata);\n\
         q.write(isender);\n\
      }\n\
      return;\n\
   }\n\
   \n\
   public boolean getMessage(ShooterThread th, float msgtype)\n\
   {\n\
      if (th.msg_queue_map == null)\n\
      {\n\
         FloatQueue q = th.msg_queue_all;\n\
         if (q.isEmpty())\n\
            return false;\n\
         if (msgtype == -1)\n\
         {\n\
            this.tf1 = q.read();\n\
            this.tf2 = q.read();\n\
            this.tf3 = q.read();\n\
            return true;\n\
         }\n\
         throw(new IllegalStateException("If you want to filter messages, use message declarations!"));\n\
         // to implement this, you would pull messages from q until done or you get a message of the correct type\n\
         // then put the irrelevant messages back\n\
      }\n\
      if (msgtype == -1)\n\
      {\n\
         for(FloatQueue q : th.msg_queue_map.values())\n\
         {\n\
            if (!q.isEmpty())\n\
            {\n\
               this.tf1 = q.read();\n\
               this.tf2 = q.read();\n\
               this.tf3 = q.read();\n\
               return true;\n\
            }\n\
         }\n\
         return false;\n\
      }\n\
      FloatQueue q = th.msg_queue_map.get((int) msgtype);\n\
      if ((q == null) || (q.isEmpty()))\n\
         return false;\n\
      this.tf1 = q.read();\n\
      this.tf2 = q.read();\n\
      this.tf3 = q.read();\n\
      return true;\n\
   }\n\
   \n\
   public static String showFloat(float f)\n\
   {\n\
      int i = (int) f;\n\
      return (f == (float) i) ? ""+i : ""+f;\n\
   }\n\
   \n\
   public boolean isDone()\n\
   {\n\
      return (this.threads.size() == 0);\n\
   }'.split("\n")
