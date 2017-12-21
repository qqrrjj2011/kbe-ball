namespace KBEngine
{
    using UnityEngine;
    using System;
    using System.Collections;
    using System.Collections.Generic;
    using System.Linq;

    public class Avatar : KBEngine.EntityCommon
    {
        public Avatar()
        {
        }

        public override void __init__()
        {
		if (isPlayer())
		{
			Event.registerIn("relive", this, "relive");
			Event.registerIn("updatePlayer", this, "updatePlayer");

			// 触发登陆成功事件
			Event.fireOut("onLoginSuccessfully", new object[] { KBEngineApp.app.entity_uuid, id, this });
		}
        }

        public override void onDestroy()
        {
            if (isPlayer())
            {
                KBEngine.Event.deregisterIn(this);
            }
        }

        public override void onEnterWorld()
        {
            base.onEnterWorld();

            if (isPlayer())
            {
                Event.fireOut("onAvatarEnterWorld", new object[] { KBEngineApp.app.entity_uuid, id, this });
            }
        }

  

        public void relive(Byte type)
        {
            cellCall("relive", type);
        }

        public virtual void updatePlayer(float x, float y, float z, float yaw)
        {
            position.x = x;
            position.y = y;
            position.z = z;

            direction.z = yaw;
        }

        public virtual void set_name(object old)
        {
            object v = getDefinedProperty("name");
            // Dbg.DEBUG_MSG(className + "::set_name: " + old + " => " + v); 
            Event.fireOut("set_name", new object[] { this, v });
        }

        public virtual void set_mass(object old)
        {
            object v = getDefinedProperty("mass");
            // Dbg.DEBUG_MSG(className + "::set_mass: " + old + " => " + v); 
            Event.fireOut("set_mass", new object[] { this, v });
        }

        public virtual void set_level(object old)
        {
            object v = getDefinedProperty("level");
            // Dbg.DEBUG_MSG(className + "::set_level: " + old + " => " + v); 
            Event.fireOut("set_level", new object[] { this, v });
        }

        public virtual void set_moveSpeed(object old)
        {
            object v = getDefinedProperty("moveSpeed");
            // Dbg.DEBUG_MSG(className + "::set_moveSpeed: " + old + " => " + v); 
            Event.fireOut("set_moveSpeed", new object[] { this, v });
        }

        public virtual void set_modelScale(object old)
        {
            object v = getDefinedProperty("modelScale");
            // Dbg.DEBUG_MSG(className + "::set_modelScale: " + old + " => " + v); 
            Event.fireOut("set_modelScale", new object[] { this, v });
        }
    }
}
