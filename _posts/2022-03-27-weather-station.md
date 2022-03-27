---
title: Weather Station 설계 (옵저버 패턴)
layout: post
date: '2022-03-27 19:21:00'
---

## **기상 스테이션 설계**
#### 클래스 다이어 그램

![weather station]({{site.url}}/assets/img/weather_station.jpg){:class="img-responsive"} 

#### 기상 스테이션 구현

```
public interface Subject {
 public void registerObserver(Observer o);
 public void removeObserver(Observer o);
 public void notifyObserver(Observer o);
}

public interface Observer {
 public void update(float temp, float humidity, float pressure);
}

public interface DisplayElement {
 public void display();
}
```

*상태를 갱신하기 위해 측정치를 직접 전달하는 것이 좋은 방법일까?
갱신된 상태를 옵저버에 전달하는 다른 좋은 방법을 고려해 보자.*

#### WeatherData에서 Subject Interface 구현하기

```
public class WeatherData implements Subject {
 private ArrayList observers;
 private float temperature;
 private float humidity;
 private float pressure;
 
 public WeatherData() {
  observers = new ArrayList();
 }
	
public void registerObserver(Observer o) {
 observers.add(o);
}
		
public void removeObserver(Observer o) {
 int i = observers.indexOf(o);
 if(i >= 0) {
  observers.remove(i);
 }
}
		
public void notifyObservers() {
 for(int i = 0; i < observers.size(); i++) {
  Observer observer = (Observer)observers.get(i);
	observer.update(temperature, humidity, pressure);
 }
}

 public void measurementChanged() {
  notifyObservers();
 }
		
public void setMeasurements(float temperature, float humidity, float pressure) {
 this.temperature = temperature;
 this.humidity = humidity;
 this.pressure = pressure;
 }
	// 기타 WeatherData method
}
```

#### Display 항목 구현하기

```
public class CurrentConditionDisplay implements Observer, DisplayElement {
	private float temperature;
	private float humidity;
	private float pressure;
		
	public CurrentCoditionDisplay (Subject weatherData) {
		this.weatherData = weatherData;
		weatherData.registerObserver(this);
	}
		
	public void update(float temperature, float humidity, float pressure) {
		this.temperature = temperature;
		this.humidity = humidity;
		display();
	}
		
	public void display() {
		System.out.println("Current coditions: " + temperature + "F degrees and " + humidity + "% humidity");
	}
}

```

#### 기상 스테이션 실행

```
public class WeathreStation {
 public static void main(String[] args) {
  WeatherData weatherData = new WeatherData();
	CurrentConditionDisplay currentDisplay = new CurrentConditionDisplay(weatherData);				
	StatisticsDisplay statisticsDisplay = new StatisticsDisply(weatherData);
	ForecastDisplay forecastDisplay = new ForecastDisplay(weatherData);
	
	weatherData.setMeasurements(80, 65, 30.4f);
	weatherData.setMeasurements(82, 70, 29.2f);
	weatherData.setMeasurements(78, 90, 29.2f);
 }
}
```
