using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class controller : MonoBehaviour
{

    public player PlayerPrefab;
    public uint NumPlayers;

    // Start is called before the first frame update
    void Start()
    {
        //player aPlayer = Instantiate(PlayerPrefab, transform) as player;
        //aPlayer.PlayerID = 1;

        for(int p = 0; p < NumPlayers; p++)
        {
            player aPlayer = Instantiate(PlayerPrefab, transform) as player;
        }
    }

    // Update is called once per frame
    void Update()
    {

    }
}
