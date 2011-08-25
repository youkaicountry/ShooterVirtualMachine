public class FloatQueue
{
   float buffer[];
   int bread, bwrite;

   public FloatQueue()
   {
      this.buffer = new float[8];
      this.bread = 0;
      this.bwrite = 0;
      return;
   }

   public static final float NO_SUCH_ELEMENT = Float.NaN;

   public float read()
   {
      if (bread == bwrite)
         return NO_SUCH_ELEMENT;
      float result = buffer[bread++];
      if (bread >= buffer.length)
         bread -= buffer.length;
      return result;
   }

   public void write(float x)
   {
      buffer[bwrite++] = x;
      if (bwrite >= buffer.length)
         bwrite -= buffer.length;
      if (bwrite == bread)
      {
         float temp[] = new float[buffer.length*2];
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

   public float[] toArray()
   {
      float result[];
      if (bwrite < bread)
      {
         result = new float[buffer.length-bread+bwrite];
         System.arraycopy(buffer, bread, result, 0, buffer.length-bread);
         System.arraycopy(buffer, 0, result, buffer.length-bread, bwrite);
      }
      else
      {
         result = new float[bwrite-bread];
         System.arraycopy(buffer, bread, result, 0, bwrite-bread);
      }
      return result;
   }
}
