import React, { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';

interface ReservationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (reservation: {
    customerName: string;
    phone: string;
    partySize: number;
    reservationTime: string;
  }) => void;
  tableNumber: number;
}

export function ReservationModal({ isOpen, onClose, onConfirm, tableNumber }: ReservationModalProps) {
  const [customerName, setCustomerName] = useState('');
  const [phone, setPhone] = useState('');
  const [partySize, setPartySize] = useState(2);
  const [reservationTime, setReservationTime] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (customerName && phone && reservationTime) {
      onConfirm({
        customerName,
        phone,
        partySize,
        reservationTime
      });
      // Reset form
      setCustomerName('');
      setPhone('');
      setPartySize(2);
      setReservationTime('');
      onClose();
    }
  };

  const timeSlots = [
    '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
    '20:00', '20:30', '21:00', '21:30', '22:00'
  ];

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px] bg-gradient-to-br from-green-50 to-yellow-50">
        <DialogHeader>
          <div className="text-center mb-2">
            <div className="text-4xl mb-2">🍽️</div>
            <DialogTitle className="text-green-700">
              Reserve Table {tableNumber}
            </DialogTitle>
            <DialogDescription>
              Feed our hungry dino! Fill in the reservation details below.
            </DialogDescription>
          </div>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="customerName">Customer Name</Label>
            <Input
              id="customerName"
              placeholder="e.g., Dr. Alan Grant"
              value={customerName}
              onChange={(e) => setCustomerName(e.target.value)}
              className="border-green-200 focus:border-green-400"
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="phone">Phone Number</Label>
            <Input
              id="phone"
              placeholder="e.g., (555) 123-DINO"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="border-green-200 focus:border-green-400"
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="partySize">Party Size</Label>
            <Select value={partySize.toString()} onValueChange={(value) => setPartySize(parseInt(value))}>
              <SelectTrigger className="border-green-200 focus:border-green-400">
                <SelectValue placeholder="How many hungry dinos?" />
              </SelectTrigger>
              <SelectContent>
                {[1, 2, 3, 4, 5, 6, 7, 8].map((size) => (
                  <SelectItem key={size} value={size.toString()}>
                    {size} {size === 1 ? 'dino' : 'dinos'} 🦕
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="reservationTime">Feeding Time</Label>
            <Select value={reservationTime} onValueChange={setReservationTime} required>
              <SelectTrigger className="border-green-200 focus:border-green-400">
                <SelectValue placeholder="When should we serve?" />
              </SelectTrigger>
              <SelectContent>
                {timeSlots.map((time) => (
                  <SelectItem key={time} value={time}>
                    {time} 🕐
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          
          <DialogFooter className="gap-2">
            <Button 
              type="button" 
              variant="outline" 
              onClick={onClose}
              className="border-gray-300 hover:bg-gray-50"
            >
              🦴 Cancel
            </Button>
            <Button 
              type="submit"
              className="bg-green-600 hover:bg-green-700 text-white"
            >
              🍖 Feed Dino!
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}