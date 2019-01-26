using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class csvread : MonoBehaviour
{
    List<coords> coords = new List<coords>();

    public Rigidbody2D rb2d;

    // Start is called before the first frame update
    void Start()
    {
        rb2d = GetComponent<Rigidbody2D> ();

        TextAsset coord_data = Resources.Load<TextAsset>("144718_1");

        string[] data = coord_data.text.Split(new char[] { '\n' });

        //string[] start_pos = data[1].Split(new char[] { ',' });

        //coords start_coord = new coords();

        //float.TryParse(start_pos[0], out start_coord.x);
        //float.TryParse(start_pos[1], out start_coord.y);

        for (int i = 1; i < data.Length - 1; i++)
        {
            string[] row = data[i].Split(new char[] { ',' });

            coords a = new coords();

            float.TryParse(row[0], out a.x);
            float.TryParse(row[1], out a.y);

            coords.Add(a);
        }

    }

    public int t = 0;

    // Update is called once per frame
    void FixedUpdate()
    {
        float move_x = coords[t].x;
        float move_y = coords[t].y;
        Vector2 movement = new Vector2(move_x,move_y);

        rb2d.transform.position = movement;

        t++;
    }
}


//using System.Collections.Generic;
//using Improbable;
//using Improbable.Gdk.Core;
//using Improbable.Gdk.Guns;
//using Improbable.Gdk.Health;
//using Improbable.Gdk.Movement;
//using Improbable.Gdk.PlayerLifecycle;
//using Improbable.Gdk.StandardTypes;
//using Improbable.PlayerLifecycle;
//using UnityEngine;

//namespace Fps
//{
//    public static class FpsEntityTemplates
//    {
//        public static EntityTemplate Spawner()
//        {
//            var position = new Position.Snapshot { Coords = new Vector3().ToSpatialCoordinates() };
//            var metadata = new Metadata.Snapshot { EntityType = "PlayerCreator" };

//            var template = new EntityTemplate();
//            template.AddComponent(position, WorkerUtils.UnityGameLogic);
//            template.AddComponent(metadata, WorkerUtils.UnityGameLogic);
//            template.AddComponent(new Persistence.Snapshot(), WorkerUtils.UnityGameLogic);
//            template.AddComponent(new PlayerCreator.Snapshot(), WorkerUtils.UnityGameLogic);

//            template.SetReadAccess(WorkerUtils.UnityGameLogic);
//            template.SetComponentWriteAccess(EntityAcl.ComponentId, WorkerUtils.UnityGameLogic);

//            return template;
//        }

//        public static EntityTemplate SimulatedPlayerCoordinatorTrigger()
//        {
//            var metadata = new Metadata.Snapshot { EntityType = "SimulatedPlayerCoordinatorTrigger" };

//            var template = new EntityTemplate();
//            template.AddComponent(new Position.Snapshot(), WorkerUtils.SimulatedPlayerCoorindator);
//            template.AddComponent(metadata, WorkerUtils.SimulatedPlayerCoorindator);
//            template.AddComponent(new Persistence.Snapshot(), WorkerUtils.SimulatedPlayerCoorindator);

//            template.SetReadAccess(WorkerUtils.SimulatedPlayerCoorindator);
//            template.SetComponentWriteAccess(EntityAcl.ComponentId, WorkerUtils.SimulatedPlayerCoorindator);

//            return template;
//        }

//        public static EntityTemplate Player(string workerId, Vector3f position)
//        {
//            var client = $"workerId:{workerId}";

//            var (spawnPosition, spawnYaw, spawnPitch) = SpawnPoints.GetRandomSpawnPoint();

//            var serverResponse = new ServerResponse
//            {
//                Position = spawnPosition.ToIntAbsolute()
//            };

//            var rotationUpdate = new RotationUpdate
//            {
//                Yaw = spawnYaw.ToInt1k(),
//                Pitch = spawnPitch.ToInt1k()
//            };

//            var pos = new Position.Snapshot { Coords = spawnPosition.ToSpatialCoordinates() };
//            var serverMovement = new ServerMovement.Snapshot { Latest = serverResponse };
//            var clientMovement = new ClientMovement.Snapshot { Latest = new ClientRequest() };
//            var clientRotation = new ClientRotation.Snapshot { Latest = rotationUpdate };
//            var shootingComponent = new ShootingComponent.Snapshot();
//            var gunComponent = new GunComponent.Snapshot { GunId = PlayerGunSettings.DefaultGunIndex };
//            var gunStateComponent = new GunStateComponent.Snapshot { IsAiming = false };
//            var healthComponent = new HealthComponent.Snapshot
//            {
//                Health = PlayerHealthSettings.MaxHealth,
//                MaxHealth = PlayerHealthSettings.MaxHealth,
//            };

//            var healthRegenComponent = new HealthRegenComponent.Snapshot
//            {
//                CooldownSyncInterval = PlayerHealthSettings.SpatialCooldownSyncInterval,
//                DamagedRecently = false,
//                RegenAmount = PlayerHealthSettings.RegenAmount,
//                RegenCooldownTimer = PlayerHealthSettings.RegenAfterDamageCooldown,
//                RegenInterval = PlayerHealthSettings.RegenInterval,
//                RegenPauseTime = 0,
//            };

//            var template = new EntityTemplate();
//            template.AddComponent(pos, WorkerUtils.UnityGameLogic);
//            template.AddComponent(new Metadata.Snapshot { EntityType = "Player" }, WorkerUtils.UnityGameLogic);
//            template.AddComponent(serverMovement, WorkerUtils.UnityGameLogic);
//            template.AddComponent(clientMovement, client);
//            template.AddComponent(clientRotation, client);
//            template.AddComponent(shootingComponent, client);
//            template.AddComponent(gunComponent, WorkerUtils.UnityGameLogic);
//            template.AddComponent(gunStateComponent, client);
//            template.AddComponent(healthComponent, WorkerUtils.UnityGameLogic);
//            template.AddComponent(healthRegenComponent, WorkerUtils.UnityGameLogic);
//            PlayerLifecycleHelper.AddPlayerLifecycleComponents(template, workerId, client, WorkerUtils.UnityGameLogic);

//            template.SetReadAccess(WorkerUtils.UnityClient, WorkerUtils.UnityGameLogic, WorkerUtils.SimulatedPlayer, WorkerUtils.AndroidClient, WorkerUtils.iOSClient);
//            template.SetComponentWriteAccess(EntityAcl.ComponentId, WorkerUtils.UnityGameLogic);

//            return template;
//        }
//    }
//}
