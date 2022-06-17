<details><summary>Docker Run</summary>
<p>

#### Send docker

```sh
   sudo docker run --entrypoint bash  --network host   -v /home/SimpleMQ_Testing:/app -it uvdeployment/shield:trt_classifier_amd64_22_06_02_nomyModule
```

```sh
   python3 python_send.py   
```


#### Receive docker

```sh
   sudo docker run --entrypoint bash  --network host   -v /home/SimpleMQ_Testing:/app -it uvdeployment/shield:trt_classifier_amd64_22_06_02_nomyModule
```


```sh
   python3 python_receive.py   
```
</p>
</details>


<details><summary>Docker Stats</summary>
<p>

#### Docker stats 

```sh
   sudo docker stats --all --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"  | grep 'Running docker name'
```

</p>
</details>


<details><summary>Valgrind</summary>
<p>

#### Valgrind command 

```sh
   valgrind  --leak-check=full \
   --show-leak-kinds=all \
   --track-origins=yes \
   --verbose \
   --log-file=valgrind-out.txt \
   python3 python_receive.py
```

</p>
</details>








