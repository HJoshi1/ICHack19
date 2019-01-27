using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class coords : MonoBehaviour
{
    public float x;
    public float y;
}

public class player : MonoBehaviour
{
    public uint PlayerID;
    // Start is called before the first frame update
    List<coords> coords = new List<coords>();

    public Rigidbody2D rb2d;

    // Start is called before the first frame update
    void Start()
    {
        rb2d = GetComponent<Rigidbody2D>();

        TextAsset coord_data = Resources.Load<TextAsset>("14110_5");

        string[] data = coord_data.text.Split(new char[] { '\n' });


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
        Vector2 movement = new Vector2(move_x, move_y);

        //rb2d.transform.position = Vector2.MoveTowards(transform.position, movement, 1);

        rb2d.transform.position = movement;

        t++;
    }
}
