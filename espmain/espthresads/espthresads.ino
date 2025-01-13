#include <Arduino.h>

void t2s(void * parameters)
{
  for(;;)
  {
    //txt2speech code
    vTaskDelay(100/portTICK_PERIOD_MS);
  }
}

void s2t(void * parameters)
{
  for(;;)
  {
    //speech2txt code
    vTaskDelay(100/portTICK_PERIOD_MS);
  }
}
void openAI(void * parameters)
{
  for(;;)
  {
    //openAI code
    vTaskDelay(100/portTICK_PERIOD_MS);
  }
}

void setup() 
{
  xTaskCreate(t2s,"t2s",1000,NULL,1,NULL);
  xTaskCreate(s2t,"s2t",1000,NULL,1,NULL);
  
  
    
  

}


