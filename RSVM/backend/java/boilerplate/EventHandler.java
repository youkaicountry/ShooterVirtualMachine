/**
 *
 * An EventHandler receives events from other VM threads or from the system.
 *
 * An event has a channel, and three data fields.  The data fields are visible
 * to the program, but the channel is used solely by the runtime.
 *
 * A channel can be regarded as equivalent to an IRQ in hardware programming,
 * that is, it identifies the specific source of the event.  The sender is the
 * ID of the sending thread, while type and data are used by the application.
 *
 * (Type is actually used by the filter mechanism to implement postponing
 * uninteresting messages.)
 */

public interface EventHandler
{
    public void handleEvent(int channel, float sender, float type, float data);
}

