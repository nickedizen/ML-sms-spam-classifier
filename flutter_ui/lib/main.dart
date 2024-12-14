import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_ui/api.dart';

void main() {
  runApp(const MainApp());
}

class MainApp extends StatefulWidget {
  const MainApp({super.key});

  @override
  State<MainApp> createState() => _MainAppState();
}

class _MainAppState extends State<MainApp> {
  String text = '';
  var data;
  String hasilPrediksi = '';

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(10.0),
            child: Center(
              child: Column(
                children: [
                  TextField(
                    onChanged: (value) {
                      text = value.toString();
                    },
                    decoration: const InputDecoration(
                      hintText: 'Masukkan pesan ...'
                    ),
                  ),
                  ElevatedButton(
                    onPressed: () async {
                      data = await predictSMS(text);
                      setState(() {
                        hasilPrediksi = data;
                      });
                    }, 
                    child: const Text('Prediksi')
                  ),
                  Text(
                    'Hasil Prediksi: $hasilPrediksi'
                  )
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
