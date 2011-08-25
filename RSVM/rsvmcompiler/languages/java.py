def constructOutputFiles(code):
    return {}

def optimize(code, options={}):
    return

def __constructMainFile():
    return

def __getBoilerPlateFiles():
    return {"EventHandler.java":bp_EventHandler, "FloatQueue.java":bp_FloatQueue, "IntQueue.java":bp_IntQueue, "ShooterThread.java":bp_ShooterThread, "ShooterVirtualMachine.java":bp_ShooterVirtualMachine}
   
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

