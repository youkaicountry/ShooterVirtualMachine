
public class IntQueue
{
   int buffer[];
   int bread, bwrite;

   public IntQueue()
   {
      this.buffer = new int[8];
      this.bread = 0;
      this.bwrite = 0;
      return;
   }

   public static final int NO_SUCH_ELEMENT = 0x80000000;

   public int read()
   {
      if (bread == bwrite)
         return NO_SUCH_ELEMENT;
      int result = buffer[bread++];
      if (bread >= buffer.length)
         bread -= buffer.length;
      return result;
   }

   public void write(int x)
   {
      buffer[bwrite++] = x;
      if (bwrite >= buffer.length)
         bwrite -= buffer.length;
      if (bwrite == bread)
      {
         int temp[] = new int[buffer.length*2];
         System.arraycopy(buffer, bread, temp, 0, buffer.length-bread);
         System.arraycopy(buffer, 0, temp, buffer.length-bread, bread);
         bread = 0;
         bwrite = buffer.length;
         buffer = temp;
      }
      return;
   }

   public boolean isEmpty()
   {
      return (bwrite == bread);
   }

   public int[] toArray()
   {
      int result[];
      if (bwrite < bread)
      {
         result = new int[buffer.length-bread+bwrite];
         System.arraycopy(buffer, bread, result, 0, buffer.length-bread);
         System.arraycopy(buffer, 0, result, buffer.length-bread, bwrite);
      }
      else
      {
         result = new int[bwrite-bread];
         System.arraycopy(buffer, bread, result, 0, bwrite-bread);
      }
      return result;
   }
}